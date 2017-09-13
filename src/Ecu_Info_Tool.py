#!coding:utf8

'''
Date:2017/8/14/9:45
Author:yqq
Description:none
'''

import os
import sys
from lib.mytool6 import MyHex
from src3.ComPin import CalcComPin   #计算引脚的算法
from lib.mytool9 import TabTextTool


gFiledKeyList = [
	"No",
	"??????", #空的
	"VehEcuId",
	"ProtocolName",
	"EnterCmd",
	"EnterReply",
	"UnKnown1",
	"BauteRate",
	"AddrCode",
	"KeepLinkCmd",
	"ComPin",
	"ReadDtcCmd",
	"DtcReply",
	"DtcBegin",
	"DtcLen",
	"Unknown2",
	"Unknown3",
	"ClearDtcCmd",
	"ClearReply",
	"?????" #空的
]





gVerInfoKeyList = [
	"???1",
	"???2",
	"EcuID",
	"???4",
	"???5",
	"???6",
	"???7",
]

gDsKeyList = [
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

gDtcKeyList = [
	"????1",
	"????2",
	"EcuID",
	"????4",
	"????5",
]

gFlagDict = {}

def GetFuncFlag():

	# inDtcFile = open("../txt/Ecu_Dtc.txt", "r")
	# inVerInfoFile = open("../txt/System_Info.txt", "r")
	# inDsFile = open("../txt/DS_Info.txt", "r")

	#tt.ShowAll()

	countVerInfoList= []
	countDsList = []
	countDtcList = []

	tt = TabTextTool("../txt/System_Info.txt", gVerInfoKeyList)
	for eachLine in tt.allNamedSplitedList:
		if int(eachLine["EcuID"].strip(), 10) <= 900010: continue
		if eachLine["EcuID"].strip() not in countVerInfoList:
			countVerInfoList.append(eachLine["EcuID"].strip())

	tt = TabTextTool("../txt/DS_Info.txt", gDsKeyList)
	# tt.ShowAll()

	for eachLine in tt.allNamedSplitedList:
		if int(eachLine["EcuID"].strip(), 10) <= 900010: continue
		if eachLine["EcuID"] not in countDsList:
			countDsList.append(eachLine["EcuID"].strip())


	tt = TabTextTool("../txt/Ecu_Dtc.txt", gDtcKeyList)
	for eachLine in tt.allNamedSplitedList:
		if int(eachLine["EcuID"].strip(), 10) <= 900010: continue
		if eachLine["EcuID"] not in countDtcList:
			countDtcList.append(eachLine["EcuID"].strip())
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(len(countDtcList)))

	for ecuId in range(900011, 900061+1):
		tmpFlagDict = {}
		if str(ecuId) in countVerInfoList:
			tmpFlagDict["VerInfoFlag"] = 1
		else:
			tmpFlagDict["VerInfoFlag"] = 0

		if str(ecuId) in countDtcList:
			tmpFlagDict["DtcFlag"] = 1
		else:
			tmpFlagDict["DtcFlag"] = 0

		if str(ecuId) in countDsList:
			tmpFlagDict["DsFlag"] = 1
		else:
			tmpFlagDict["DsFlag"] = 0

		gFlagDict[ecuId] = tmpFlagDict

	return gFlagDict




def ReadTabTextFile(filePath):

	'''
	:param filePath: 输入文件路径
	:return: 读取以tab分隔的文件内容,以列表形式
	'''

	if os.path.isfile(filePath):
		outFile = open("../doc/tmp/out_Ecu_Info.txt", "w")
		with open(filePath, "r") as inFile:
			inFileContList =  inFile.readlines()
			for eachLine in inFileContList:
				if len(eachLine) == 0:
					continue
				if '\t' in eachLine:
					splitedList = eachLine.split("\t")
					print("==================")
					if (int(splitedList[2], 10) <= 900010) | (splitedList[3] == '0x200019'):  #屏蔽小于等于900010的(没开发)
						continue
					indexStr = MyHex(int(splitedList[2], 10) - 900000)
					outFile.write("0xFF,0xFF,0xFF,0xFF,0xFF,{0}\t\t\"\\\n".format(indexStr))
					outFile.write("[Netlayer]\t\t\t\t\t\\n\\\n")

					#print(len(splitedList))
					for i in range(0, len(splitedList)):
						if (1 == i) | (0 == i): continue
						#print("{0}={1}".format("\t????" ,  splitedList[i]))
						print("{0}={1}".format("\t" + gFiledKeyList[i], splitedList[i]))

						#2017-09-11 加上两个自定义的字段, EcuId 和 ToolId
						if True:
							if gFiledKeyList[i] == "EnterCmd":
								if splitedList[3].strip() == "CAN":
									EcuID = splitedList[i].strip()[:4]
									ToolID = splitedList[i + 1].strip()[:4]
									outFile.write("\tEcuId={0}\t\t\t\t\t\\n\\\n".format(EcuID))
									outFile.write("\tToolId={0}\t\t\t\t\t\\n\\\n".format(ToolID))

									outFile.write("{0}={1}\t\t\t\t\t\\n\\\n".format(
										"\t" + gFiledKeyList[i], splitedList[i].strip()[6:]))
									continue
									pass
								elif "KWP" in splitedList[3].strip():
									EcuID = splitedList[i].strip()[2:4]
									ToolID = splitedList[i].strip()[4:6]
									outFile.write("\tEcuId={0}\t\t\t\t\t\\n\\\n".format(EcuID))
									outFile.write("\tToolId={0}\t\t\t\t\t\\n\\\n".format(ToolID))

									if splitedList[3].strip() == "KWP2000":
										outFile.write("{0}={1}\t\t\t\t\t\\n\\\n".format(
											"\t" + gFiledKeyList[i], splitedList[i].strip()[6:-2]))
									elif splitedList[3].strip() == "KWP_0X":
										outFile.write("{0}={1}\t\t\t\t\t\\n\\\n".format(
											"\t" + gFiledKeyList[i], splitedList[i].strip()[2:6]))
									else:
										outFile.write("{0}={1}\t\t\t\t\t\\n\\\n".format(
											"\t" + gFiledKeyList[i], splitedList[i].strip()))
										pass
									continue
								else:
									raise ValueError
								pass


						outFile.write("{0}={1}\t\t\t\t\t\\n\\\n".format(
							"\t" + gFiledKeyList[i], splitedList[i]))

						#2017-09-11  追加3个自定义的字段, 分别标识故障码,版本信息,数据流功能是否存在
						if i + 2 == len(splitedList):  #最后一个

							tmpEcuId = int(splitedList[2].strip(), 10)
							if tmpEcuId in gFlagDict:
								outFile.write("\t"+"{0}={1}\t\t\t\t\t\\n\\\n".format("VerFuncFlag", gFlagDict[tmpEcuId]["VerInfoFlag"]))
								outFile.write("\t" + "{0}={1}\t\t\t\t\t\\n\\\n".format("DtcFuncFlag", gFlagDict[tmpEcuId]["DtcFlag"]))
								outFile.write("\t" + "{0}={1}\t\t\t\t\t\\n\"\n\n".format("DsFuncFlag", gFlagDict[tmpEcuId]["DsFlag"]))

							break
						else:
							continue
							#outFile.write("\\\n")

		outFile.close()
	else:
		print("error in ReadTabTextFile(): filePath is not a file.")
	pass




def main():

	GetFuncFlag()
	ReadTabTextFile("../txt/Ecu_Info.txt")

	pass

if __name__ == "__main__":

	main()

	pass