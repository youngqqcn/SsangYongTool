#!coding:utf8

'''
Date:2017/9/26/8:51
Author:yqq
Description: 为测试数据流造数据
'''
from collections import OrderedDict
from lib.mytool10 import TabTextTool
from lib.mytool10 import TextTool

from random import  randint    #用于随机生成测试数据
import os
import shutil   #复制和删除文件


gVehEcuIdList = []

gDsFilPath = "../txt/DS_Info.txt"
#gDsCmd = "67 68 69 6A 6B 6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 66 67 68 69 6A 6B 6C 86 87 88 89 8A 8B 8C 8D 8E 8F 90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6"
gDsCmd = ''


gDsFieldNameList = [
		"NO",
		"????0",  # 无用
		"EcuId",
		"????1",  # 无用
		"????2",  # 无用
		"DsName",
		"DsCmd",
		"Reply",
		"CtrlByte",
		"Length",
		"k1",
		"k2",
		"k3",  # ??
		"k4",  # ??
		"DsMode",
		"????4",  # ???
		"????5",  # ???
		"DsUnit",  #
		"????7"  # 无用
]



def ReadData(inArg1, inArg2):
	'''
	:return: 获取到的故障码数据   
	数据结构: {EcuId1:[{field1:value1, field2:value2,..}, {}, {}], EcuId2:[...]}
	'''

	tt = TabTextTool(inArg1, inArg2)

	retDict = OrderedDict()
	# for i in range(900001, 900061+1):
	# 	retDict[str(i)] = []
	for lineDict in tt.allNamedSplitedList:
		#print(lineDict["EcuId"])
		if lineDict["EcuId"] not in retDict:
			retDict[lineDict["EcuId"]] = []
		retDict[lineDict["EcuId"]].append(lineDict)
	return retDict



def GenCmd(inLen = 64):
	'''
	随机生成回复命令 
	:return: 
	'''

	retCmd = ''
	for i in range(inLen):
		tmp = randint(0, 0xff+1)
		retCmd += ("%02x"%tmp).upper()
	return retCmd




def AddSpace(inStr ):
	'''
	:param inStr: 
	:return: 
	'''
	return ''.join(" " + inStr[i * 2: i * 2 + 2]   for i in range(len(inStr) / 2))[0: ]


	pass



def MakeAnsCmd(protName, ecuId, toolId, keyWord):
	'''
	:param protName: 
	:param ecuId: 
	:param toolId: 
	:return: 
	'''

	if protName.upper() == "KWP2000":
		#return  "BF " + toolId+ " "+ ecuId+ " " + keyWord + " "+ gDsCmd
		return  "BF " + toolId+ " "+ ecuId+ " " + keyWord + " "+ AddSpace(GenCmd())

	#if protName.upper == "CAN":

	pass



def GetEnterCmd():
	'''
	从EcuInfo.txt中获取进入命令
	:return: 
	'''
	tmpKeyList = ["VehEcuId", "EnterCmd"]
	tt = TabTextTool("../txt/EnterCmd.txt", tmpKeyList)

	retDict = {}

	nList  = tt.allNamedSplitedList

	for eachLine in nList:
		retDict[eachLine["VehEcuId"]] = eachLine["EnterCmd"]

	return retDict


def GetCanDsAnsCmd(ecuId, toolId, keyWord):
	'''
	:param ecuId: 
	:param toolId: 
	:param keyWord: 
	:return: 
	'''
	retCmd = ''

	retCmd += "Ans: " +  AddSpace( toolId + "08103E" + keyWord + GenCmd(5) ) + "\n"
	retCmd += "Req: " + AddSpace(ecuId +  "0830" + "00"*7 ) + "\n"

	for i in range(21, 28+1):
		retCmd += "Ans: " + AddSpace(toolId + "08" + str(i) + GenCmd(7)) + "\n"

	retCmd += "\n"

	return retCmd




def main(dirName):

	retEnterCmdDict  = GetEnterCmd()

	#global  gDsCmd
	#gDsCmd = AddSpace(GenCmd()) #生成随机数据




	# 获取数据流数据
	dsDict = ReadData(gDsFilPath, gDsFieldNameList)

	ecuDict = TextTool("../doc/tmp/out_Ecu_Info_new.txt")

	CtrlDsCmdDict= {}  #用来保存已经生成过的数据流命令
	enterCmdFlag = False  #控制进入命令有写入一次
	allSectDict = ecuDict.allSectDictOfFile
	for sectKey in allSectDict:
		sectDict = allSectDict[sectKey]["Netlayer"]
		vehEcuId = sectDict["VehEcuId"][0].strip()
		protName = sectDict["ProtocolName"][0].strip()
		ecuId = sectDict["EcuId"][0].strip()
		toolId = sectDict["ToolId"][0].strip()
		dsFlag = sectDict["DsFuncFlag"][0].strip()
		#enterCmd = sectDict["EnterCmd"][0].strip()

		with open(dirName + "/{0}.txt".format(str(vehEcuId)), "a+") as outFile:

			if vehEcuId not in CtrlDsCmdDict:
				CtrlDsCmdDict[vehEcuId] = []
				enterCmdFlag = True

			if (protName.upper() == "KWP_0X") | (protName.upper() == "KWP2000(5BPS)"):
				continue

			if (protName.upper() == "CAN"):
				if int(dsFlag, 10) == 1:

					if vehEcuId not in gVehEcuIdList:
						gVehEcuIdList.append(vehEcuId)

					for eachLineDict in dsDict[vehEcuId]:
						# 系统进入命令

						tmpEnterCmd = "Req: " + AddSpace(retEnterCmdDict[vehEcuId][0:4] + "08" + retEnterCmdDict[vehEcuId][4:] + '00' * (7 - int(retEnterCmdDict[vehEcuId][4:6], 16)))
						keyWord = hex(int(retEnterCmdDict[vehEcuId].strip()[6: 8], 16) + 0x40)[2:]
						tmpEnterReply = "Ans: " + AddSpace(toolId + "08" + "07" + keyWord + ("00" * 6))

						# 生成CAN数据流命令
						tmpDsReqCmd = "Req: " + AddSpace(eachLineDict["DsCmd"][0:4] + "08" + eachLineDict["DsCmd"].strip()[4:] + '00' * (7 - int(eachLineDict["DsCmd"].strip()[4:6], 16)))
						keyWord = hex(int(eachLineDict["DsCmd"].strip()[6: 8], 16) + 0x40)[2:]
						tmpDsAnsCmd = GetCanDsAnsCmd(ecuId, toolId, keyWord)

						# 控制每条数据流命令只有一个回复
						if eachLineDict["DsCmd"].strip() not in CtrlDsCmdDict[vehEcuId]:
							CtrlDsCmdDict[vehEcuId].append(eachLineDict["DsCmd"].strip())
						else:
							continue
						if enterCmdFlag:
							outFile.write("\n\n{0}\n{1}\n\n".format(tmpEnterCmd, tmpEnterReply))
							enterCmdFlag = False
						outFile.write("\n\n{0}\n{1}\n".format(tmpDsReqCmd, tmpDsAnsCmd))
					continue
					pass

			# 80 系列
			if (vehEcuId == "900024") | (vehEcuId == "900050") | (vehEcuId == "900061"):
				# 900024 和 900061都没有数据流
				# 900050系统进不去
				if int(dsFlag, 10) == 1:
					continue
				pass

			# {EcuId1:[{field1:value1, field2:value2,..}, {}, {}], EcuId2:[...]}
			if protName.upper() == "KWP2000":
				if int(dsFlag, 10) == 1:

					if vehEcuId not in gVehEcuIdList:
						gVehEcuIdList.append(vehEcuId)

					for eachLineDict in dsDict[vehEcuId]:
						try:
							tmpDsReqCmd = "Req: " + AddSpace(eachLineDict["DsCmd"].strip())
							keyWord = hex(int(eachLineDict["DsCmd"].strip()[6: 8], 16) + 0x40)[2:]
							tmpDsAnsCmd = "Ans: " + MakeAnsCmd(protName, ecuId, toolId, keyWord)

							tmpEnterCmd = "Req: " + AddSpace(retEnterCmdDict[vehEcuId].strip())
							keyWord = hex(int(tmpEnterCmd.strip()[6: 8], 16) + 0x40)[2:]
							tmpEnterReply = "Ans: " + MakeAnsCmd(protName, ecuId, toolId, keyWord)

							# 控制每条数据流命令只有一个回复
							if eachLineDict["DsCmd"].strip() not in CtrlDsCmdDict[vehEcuId]:
								CtrlDsCmdDict[vehEcuId].append(eachLineDict["DsCmd"].strip())
							else:
								continue
							if enterCmdFlag:
								outFile.write("\n\n{0}\n{1}\n".format(tmpEnterCmd, tmpEnterReply))
								enterCmdFlag = False
							outFile.write("\n\n{0}\n{1}\n".format(tmpDsReqCmd, tmpDsAnsCmd))
						except:
							pass


	pass



def MyCopy():
	'''
	将生成的命令文件,copy到一个指定的目录下面
	:return: 
	'''
	dirName = ""
	if not os.path.exists("../doc/out_DsTest"):
		os.mkdir("../doc/out_DsTest")
	for i in range(1, 100):
		if not os.path.exists("../doc/out_DsTest/DsTest{0}".format(str(i))):
			dirName = "../doc/out_DsTest/DsTest{0}/".format(str(i))
			shutil.copytree("../doc/out_CarData", dirName)
			break
	return dirName



def MyDel(dirName):
	'''
	:param dirName: 
	:return: 
	'''

	fileNameList  = os.listdir(dirName)
	for name in fileNameList:   #name 是带后缀的
		if os.path.splitext(name)[0] not in gVehEcuIdList:
			os.remove(dirName + "/" + name)  #删除没用的文件
			pass
	pass


if __name__ == "__main__":

	# if os.path.exists("../doc/out_DsTest") :
	# 	shutil.rmtree("../doc/out_DsTest")
	dirName = MyCopy()
	main(dirName)
	MyDel(dirName)

	pass