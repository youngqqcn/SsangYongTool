#!coding:utf8

'''
Date:2017/9/6/17:57
Author:yqq
Description: 统计有版本信息功能的Ecu个数
'''

from lib.mytool9 import TabTextTool

gKeyList = [
	"???1",
	"???2",
	"EcuID",
	"???4",
	"???5",
	"???6",
	"???7",
]



def main():

	tt = TabTextTool("../txt/System_Info.txt", gKeyList)
	#tt.ShowAll()

	countEcuIDList = []

	for eachLine in tt.allNamedSplitedList:
		if eachLine["EcuID"].strip() not in countEcuIDList:
			countEcuIDList.append(eachLine["EcuID"].strip())

	print(len(countEcuIDList))

	pass


if __name__ == "__main__":

	main()

	pass