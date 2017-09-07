#!coding:utf8

'''
Date:2017/9/7/9:22
Author:yqq
Description:统计有数据流功能的ECU个数
'''

from lib.mytool9 import TabTextTool

gFieldNameList = [
	"NO",
	"NO-USE", #无用
	"EcuID",
	"NO-USE", #侦测命令??
	"NO-USE", #侦测命令回复??
	"DsName",
	"DsCmd",
	"Reply",
	"CtrlByte",
	"Length",
	"k1",
	"k2",
	"k3",#??
	"k4",#??
	"DsMode",
	"????4",#???
	"????5",#???
	"DsUnit",
	"NO-USE" #无用
]


def main():

	tt = TabTextTool("../txt/DS_Info.txt", gFieldNameList)
	#tt.ShowAll()

	counList = []
	for eachLine in tt.allNamedSplitedList:
		if int(eachLine["EcuID"].strip(), 10) <= 900010: continue
		if eachLine["EcuID"] not in counList:
			counList.append(eachLine["EcuID"])
	print(len(counList))
	pass


if __name__ == "__main__":

	main()

	pass