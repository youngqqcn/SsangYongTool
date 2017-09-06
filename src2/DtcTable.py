#!coding:utf8

'''
Date:2017/8/24/17:15
Author:yqq
Description: 填故障码表工具
'''

import  os
import sys
import traceback
from collections import OrderedDict
from lib.mytool6 import TabTextTool
from lib.mytool6 import Add0x
from lib.mytool6 import TextTool
#from lib.mytool6 import ReadText
from lib.mytool9 import MyHexPlusPlus


def ReadText2(inFilePath):
	'''
	:param inFilePath: 读inFilePath文件, 如CN_TEXT.txt
	:return: 返回一个字典(按插入顺序排序)
	'''
	if os.path.isfile(inFilePath):
		with open(inFilePath, "r") as lan:
			linesList = lan.readlines()
		# retLanDict = {}
		retLanDict = OrderedDict()
		for line in linesList:
			if line != "\n":
				key = line.split("\t\t")[0]

				tmpStr = line.split("\t\t")[1]
				pcbuCode = tmpStr[tmpStr.find("\"") + 1: tmpStr.rfind("\"")].strip()

				tmpStr = line.split("\t\t")[2]
				dtcText = tmpStr[tmpStr.find("\"") + 1: tmpStr.rfind("\"")].strip()

				retLanDict[key] = (pcbuCode, dtcText)   #元组
		return retLanDict





def ReadDtcFile(dtcTextDict, outFile, dtcCmdDict):

	'''
	:param dtcTextDict:  故障码文本字典
	:param outFile:  输出文件对象
	:param dtcCmdDict:  故障码命令字典
	:return:  无 
	
	大部分故障码的前缀是: 0x55,0x43,0x67,0xA0, + 故障码序号转成16进制(补齐两个字节)
	900011的前缀是: 0x55,0x05,0x06,0x00,  +  码号(回复的内容)    
	
	一般情况下是优先在  0x55,0x43,0x67,0xA0, 范围内查找;
	 如果找不到,再去0x55,0x05,0x06,0x00, 范围查找  (有些则不会)
	
	'''

	# for key, tp in retDict.items():
	# 	try:
	# 		print("{0} {1} {2}\n".format(key, tp[0], tp[1]))
	# 	except:
	# 		traceback.print_exc()

	keyNameList = [
		"No",
		"NO-USE",
		"EcuID",
		"DtcCode",  #故障码码号
		"DtcNo",  #故障码序号
	]

	tt = TabTextTool("../txt/Ecu_Dtc.txt", keyNameList)
	#tt.ShowAll()

	for eachLineDict in tt.allNamedSplitedList:

		tmpEcuId = eachLineDict["EcuID"].strip()
		if int(tmpEcuId, 10) <= 900010:
			continue

		tmpDtcCode = eachLineDict["DtcCode"].strip()  #获取故障码码号
		tmpDtcNo = eachLineDict["DtcNo"].strip() #获取故障码序号

		if tmpEcuId == '900011':
			tmpIndex = "0x55,0x05,0x06,0x00," + Add0x(tmpDtcCode)  #前缀 + 码号
		else:
			tmpIndex = '0x55,0x43,0x67,0xA0,' + MyHexPlusPlus(tmpDtcNo, 2)   # 前缀 + 序号(需转换)

		if tmpIndex in dtcTextDict:
			tmpPcbuCode = dtcTextDict[tmpIndex][0].strip()
			tmpDtcText = dtcTextDict[tmpIndex][1].strip()
			if tmpDtcText == "":
				tmpDtcText = " "  #赋值为空格, 保持Excel表格的格式整洁
		else:
			continue
		if tmpEcuId in dtcCmdDict:
			tmpDtcCmd = dtcCmdDict[tmpEcuId]
		else:
			#print(tmpEcuId) #[900025, 900026, 900027]
			continue

		outFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(
			tmpEcuId, tmpPcbuCode, tmpDtcText, tmpDtcCmd, tmpDtcCode, tmpDtcNo
		))

	pass




def main():

	tt = TextTool("../doc/tmp/out_Ecu_Info.txt")
	#tt.ShowAll()

	dtcCmdDict = OrderedDict()
	allSectDict = tt.allSectDictOfFile

	for sectKey in allSectDict:
		for filedKey, filedDict in allSectDict[sectKey].items():
			if "ReadDtcCmd" in filedDict:
				dtcCmdDict[filedDict["EcuId"][0].strip()] = filedDict["ReadDtcCmd"][0].strip()

	inFilePath = "../txt/cn_dtc.txt"
	outFilePath = "../doc/tmp/out_Dtc_Table.txt"

	dtcTextDict = ReadText2(inFilePath)   #获取原始故障码库
	with open(outFilePath, "w") as outFile:
		ReadDtcFile(dtcTextDict, outFile, dtcCmdDict)

	pass




if __name__ == "__main__":

	main()

	pass