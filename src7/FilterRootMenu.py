#!coding:utf8

'''
Date:2017/9/30/14:27
Author:yqq
Description: 过滤菜单,  去掉KWP2000(5bps)协议的ECU 

'''



import  os

gEcuIdProtocalDict = {}  #需要过滤的EcuId

def GetEcuIdProtocal():
	'''
	:return:  解析Ecu_Info.txt获取 ECU 和 协议类型组成的字典
	'''

	with open("../txt/Ecu_Info.txt", "r") as inFile:
		lineList = inFile.readlines()
		for eachLine in lineList:
			splitedList = eachLine.split("\t", 4)[2 : 4]
			if splitedList[0] not in gEcuIdProtocalDict:
				if ("5bps" in  splitedList[1]) | ("_0X" in splitedList[1]):
					gEcuIdProtocalDict[splitedList[0]] = splitedList[1]
			#print(splitedList)
	pass


def FilterRootMenuText(language):
	'''
	:param language: 语言
	:return: 去掉了KWP2000(5bps)的ECU
	'''

	retLineBuf = []
	with open("../txt/{0}_ROOT.txt".format(language), "r") as inFile:

		lineList = inFile.readlines()

		for eachLine in lineList:
			if ('<' in eachLine) & ('>' in eachLine):
				ecuId = eachLine[eachLine.find('<') + 1 : eachLine.find('>')].strip()
				if ecuId in gEcuIdProtocalDict:
					continue
			retLineBuf.append(eachLine)
	return retLineBuf




def DelSingleSysName(lineBuf, language, recurDeepth = 3):
	'''
	:param lineBuf:  处理后的 行
	:param language:  语言
	:param recurDeepth:  默认递归3次, 足矣
	:return: 
	'''

	if recurDeepth == 0:
		if os.path.exists("../doc/tmp/new_{0}_ROOT.txt".format(language)):
			os.remove("../doc/tmp/new_{0}_ROOT.txt".format(language))

		with open("../doc/tmp/new_{0}_ROOT.txt".format(language), "w") as outFile:
			outFile.writelines(lineBuf)
		return

	#删除 只有一个系统名的系统
	retLineBuf = []
	for i in range(len(lineBuf)):
		if ('<' not in lineBuf[i]) & ('>' not in lineBuf[i]):
			if i + 1 >= len(lineBuf):  # 最后一行
				continue
			if (lineBuf[i].count('\t') >= lineBuf[i + 1].count('\t')):
				continue
		retLineBuf.append(lineBuf[i])

	DelSingleSysName(retLineBuf, language, recurDeepth - 1)   #默认递归3次, 彻底清除没有ECU的系统名




def main():




	lanList = []
	if os.path.exists("../txt/EN_ROOT.txt"):  #英文
		lanList.append("EN")
	if os.path.exists("../txt/CN_ROOT.txt"):  #中文
		lanList.append("CN")

	if len(lanList) == 0:
		raise ValueError

	GetEcuIdProtocal()   #获取需要过滤的ecuID, 与语言无关

	for eachLan in lanList:
		retLineBuf =  FilterRootMenuText(eachLan)
		DelSingleSysName(retLineBuf, eachLan)

	pass


if __name__ == "__main__":

	main()

	pass