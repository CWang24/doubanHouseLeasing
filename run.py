#!/user/bin/env python
# -*- coding: utf-8 -*-
__author__="YYYY"   

import re
import urllib.request
import urllib.parse
from urllib.parse import quote
import string
import os
import datetime

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

def isGoodDate(date_old, deltaDaysLimit):
	yyyy = int(date_old.split('-')[0])
	mm = int(date_old.split('-')[1])
	dd = int(date_old.split('-')[2])
	date_old_fmt = datetime.date(yyyy, mm, dd)
	date_new_fmt = datetime.date.today()
	deltaDays = (date_new_fmt - date_old_fmt).days
	if deltaDays > deltaDaysLimit:
		#print('Too early')
		return False
	else:
		return True


def dowmlpad(url, user_agent='wswp', proxy=None, num_retries=2, timeout=5):
	print('DownloadURL:',url)

	#配置用户代理
	headers = {'User-agent':user_agent}
	request = urllib.request.Request(url, headers=headers)
	#配置
	opener = urllib.request.build_opener()

	#判断是否代理
	if proxy:
		proxy_params = {urllib.parse.urlparse(url).scheme:proxy}
		opener.add_handler(urllib.request.ProxyHandler(proxy_params))
	try:
		html = opener.open(request, timeout=timeout).read()
	except urllib.request.URLError as e:
		print('Download error:',e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e,'code') and 500 <= e.code <600:
				html = dowmlpad(url, user_agent, num_retries-1)
	except Exception as e:
		print('error :',e)
		html = None

	return html
	
def inBlackList(title2Btested):
	#blacklist = ["川杨新苑", "玉兰香苑", "求租", "北蔡"]
	blacklist = ["同济"]
	for blacklist_word in blacklist:
		if blacklist_word in title2Btested:
			return True
	return False

def inDoubanGroupList(groupName):
	DoubanGroupList = ["zjhouse", "homeatshanghai", "pudongzufang", "shanghaizufang", "shzf", "173252", "467799", "492107", "496399", "513885", "531553", "558784", "558817", "580888", "583132", "583601" "597660", "599811"]
	
	if groupName in DoubanGroupList:
		return True
	else:
		return False
	
def get50entriesSearchResult(input_lines, output_lines):
	lines = input_lines
	#output_lines = []
	inside_table = 0
	count = 0
	dup_flag = 0
	all_too_early_flag = 1
	#date = ''
	for line in lines:
		
		line = line.rstrip()
		line_str = line.decode()
		# print(line)
		if '<table class="olt">' in line_str:
			inside_table = 1
			#print('start threads')
	
		if '</table>' in line_str and inside_table == 1:
			inside_table = 0
			#print('stop threads')
		
		if inside_table == 1:
			# fout.write(line_str)
			p1 = re.compile(r'.*td-subject.*href="(.*)" onclick.* title="(.*)"')
			m1 = re.match(p1, line_str)
			p2 = re.compile(r'.*td-time.*title="(.*) .*" ')
			m2 = re.match(p2, line_str)
			p3 = re.compile(r'.*<td><a href="https://www.douban.com/group/(.*)/" class.*')
			m3 = re.match(p3, line_str)
			if m1:
				href = m1.group(1)
				title = m1.group(2)
				if title in titles:
					# print('duplicated')
					dup_flag = 1
					continue
				elif inBlackList(title):
					dup_flag = 1
					continue
				else:
					titles.append(title)
					dup_flag = 0
				# print(href)
				# print(title)
				
				line_new = '<a href="'+href+'" class="">'+title+'</a>'
				
				# print(line_new)
				# fout.write(line_new+'\n')
				output_lines.append(line_new)
			elif m2:
				if dup_flag == 0 :
					date = m2.group(1)
					if isGoodDate(date, 50):
						all_too_early_flag = 0
						line_new = '<a>'+date+'</a><br>'
						# fout.write(line_new+'\n')
						output_lines.append(line_new)
						# print(date)
						count = count + 1
					else:
						del output_lines[-1]
			elif m3: 
				if dup_flag == 0 :
					#print(line_str)
					if isGoodDate(date, 50):
						groupName = m3.group(1)
						if inDoubanGroupList(groupName):
							#output_lines.append(line_str)
							pass
						else:
							del output_lines[-1]
							del output_lines[-1]
					
	# fout.close()
	print('Stored '+ str(count) + ' results.\n')
	return all_too_early_flag
	
	
def getRecentSearchResultOfXiaoqu(xiaoqu):
	output_lines = []
	page = 0
	all_too_early_flag = 0
	#for page in pages:
	while all_too_early_flag == 0:
		page_str = str(page)
		print("Browsing page"+page_str+' with following 50 entries of xiaoqu '+xiaoqu)
		url = 'https://www.douban.com/group/search?start='+page_str+'&cat=1013&sort=time&q='+xiaoqu+''
		s = quote(url,safe=string.printable)
		html = dowmlpad(s)
		
		f = open(xiaoqu+'.raw.html', 'wb')
		f.write(html)
		f.close()
		
		f = open(xiaoqu+'.raw.html', 'rb')
		input_lines = f.readlines()
		f.close()
		
		all_too_early_flag = get50entriesSearchResult(input_lines, output_lines)
		page = page+50
		
	fout = open(xiaoqu+'.html', 'w', errors="ignore")
	for line in output_lines:
		try:
			fout.write(line+'\n')
		except:
			print(line)
	fout.close()
	
if __name__ == '__main__':
	titles = []
	#xiaoqus = ["流明新苑", "兰沁苑", "樟盛苑", "香楠小区", "张江人才公寓", "广兰丽园", "中芯花园", "申源苑", "春港丽园"]
	xiaoqus = ["古桐", "建中路"]
	for xiaoqu in xiaoqus:
		getRecentSearchResultOfXiaoqu(xiaoqu)

	os.system('rm -f *raw.html')
	
