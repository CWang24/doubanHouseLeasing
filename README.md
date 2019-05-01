# doubanHouseLeasing

It's basically a crawler script that helps sift out noise information from massive duplications of posting by either agent or sub-leaser.
Run this python script, one webpage will be generated for each community you input, which contains all posting of house leasing in the last certain days. The script is rough yet useful. I ran it once per day each night, and well organized lists were presented.

## Brief Tutorial:

### In main, set the xiaoqu that you are interested in.
xiaoqus = ["", ""]
### In "inDoubanGroupList", set the douban Groups that people submit house leasing information.
DoubanGroupList = ["zjhouse", "homeatshanghai", "pudongzufang", "shanghaizufang", "shzf", "173252", "467799", "492107", "496399", "513885", "531553", "558784", "558817", "580888", "583132", "583601" "597660", "599811"]
### In "inBlackList", set the names once appear, whose post should be skipped.
blacklist = [" ", " ", " ", " "]

### In "isGoodDate", set the upper limit of days of posting that you want to list.
if isGoodDate(date, 50):
