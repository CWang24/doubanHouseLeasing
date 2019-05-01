# doubanHouseLeasing

It's basically a crawler script, that helps sift out noise informations from massive duplication of posting by either agents or sub-leaser.
Run this python script, one webpage will be generated for each xiaoqu you put, which contains all posting of house leasing in last certain days. The script is rough yet useful. I ran it once per day each night. It saved time, and make thing organized.

## Brief Tutorial:

### In main, set the xiaoqu that you are interested in.
xiaoqus = ["", ""]
### In "inDoubanGroupList", set the douban Groups that people submit house leasing information.
DoubanGroupList = ["zjhouse", "homeatshanghai", "pudongzufang", "shanghaizufang", "shzf", "173252", "467799", "492107", "496399", "513885", "531553", "558784", "558817", "580888", "583132", "583601" "597660", "599811"]
### In "inBlackList", set the names once appear, whose post should be skipped.
blacklist = [" ", " ", " ", " "]

### In "isGoodDate", set the upper limit of days of posting that you want to list.
if isGoodDate(date, 50):
