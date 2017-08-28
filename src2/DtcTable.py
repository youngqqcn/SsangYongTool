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
	:param inFilePath:  故障码文件 
	:return: 
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
		"DtcCode",
		"??No1??",
	]

	tt = TabTextTool("../txt/Ecu_Dtc.txt", keyNameList)
	#tt.ShowAll()

	for eachLineDict in tt.allNamedSplitedList:

		tmpEcuId = eachLineDict["EcuID"]
		if int(tmpEcuId, 10) <= 900010:
			continue
		tmpDtcCode = eachLineDict["DtcCode"]
		tmpIndex = "0x55,0x05,0x06,0x00," + Add0x(tmpDtcCode)
		if tmpIndex in dtcTextDict:
			tmpPcbuCode = dtcTextDict[tmpIndex][0]
			tmpDtcText = dtcTextDict[tmpIndex][1]
			if tmpDtcText == "":
				tmpDtcText = " "
		else:
			continue
		tmpDtcCmd = dtcCmdDict[tmpEcuId]

		outFile.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(
			tmpEcuId, tmpPcbuCode, tmpDtcText, tmpDtcCmd, tmpDtcCode
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
				dtcCmdDict[filedDict["EcuId"][0]] = filedDict["ReadDtcCmd"][0].strip()

	inFilePath = "../txt/cn_dtc.txt"
	outFilePath = "../doc/tmp/out_Dtc_Table.txt"

	dtcTextDict = ReadText2(inFilePath)
	with open(outFilePath, "w") as outFile:
		ReadDtcFile(dtcTextDict, outFile, dtcCmdDict)

	pass




if __name__ == "__main__":

	main()

	pass