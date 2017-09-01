#!coding:utf8

'''
Date:2017/8/24/11:35
Author:yqq
Description: 填ECU表的工具
'''

from lib.mytool6 import TextTool
from lib.mytool6 import MyHex
from lib.mytool6 import Add0x
from lib.mytool6 import Del0x
from collections import OrderedDict
from src3.ComPin import CalcComPin

def ReadRootMenuFile(inFilePath):
	'''
	:param inFilePath:  输入的root菜单文件路径
	:return:  一个菜单树(字典)
	
	数据结构:  
	{
		Car1 : {
			Sys1 : {
				EcuName1 : [EcuID1, EcuID2, ...]
				EcuName2 : [EcuID1, ...]
				...
			},
			Sys2 : {
				EcuName1 : [EcuID1, EcuID2, ...]
				EcuName2 : [EcuID1, ...]
				...
			},
			...
		},
		
		Car2 : {
			...
		}, 
		
		...
	}
	
	'''

	retDict = OrderedDict()
	with open(inFilePath, "r") as inFile:
		rootList = inFile.readlines()
		tmpSysName = ""
		tmpCarName = ""
		tmpEcuName = ""
		for eachLine in rootList:
			if eachLine == "":
				break

			if eachLine.count("\t") == 1:  #只有一个制表符,是车型名
				tmpCarName = eachLine.strip() #去掉两边的空白符
				retDict[tmpCarName] = OrderedDict()
				tmpSysName = ""
				tmpEcuName = ""
			elif eachLine.count("\t") == 2: #有两个制表符, 是系统名
				if "<9000" in eachLine:  #没有下一级
					tmpStr = eachLine.strip()
					tmpSysName = tmpStr[0 : tmpStr.find("<9000")]
					tmpEcuId = tmpStr[tmpStr.find("<9000") + 1: -1]
					tmpEcuName = tmpSysName #特殊处理, 加一层
					retDict[tmpCarName][tmpSysName] = OrderedDict()
					retDict[tmpCarName][tmpSysName][tmpEcuName] = [tmpEcuId]
					#tmpSysName = ""
					#tmpEcuName = ""
				else: #还有下一级
					tmpSysName = eachLine.strip()
					retDict[tmpCarName][tmpSysName] = OrderedDict()

					continue
			elif eachLine.count("\t") == 3: #有3个制表符, 是Ecu名
				if "<9000" in eachLine: #说明没有下一级了
					tmpStr = eachLine.strip()
					tmpEcuName = tmpStr[0 : tmpStr.find('<9000')] #获取Ecu名
					tmpEcuId = tmpStr[tmpStr.find('<9000') + 1 : tmpStr.find(">")] #获取EcuId
					retDict[tmpCarName][tmpSysName][tmpEcuName] = [tmpEcuId]
				else:
					#一个有两个ECUID
					tmpEcuName = eachLine.strip()
					retDict[tmpCarName][tmpSysName][tmpEcuName] = []
					continue
			elif eachLine.count("\t") == 4: #子ECU
				tmpStr = eachLine.strip()
				tmpName = tmpStr[0 : tmpStr.find("<9000") - 1]
				tmpEcuId = tmpStr[tmpStr.find("<9000") + 1 : -1]
				if tmpName in retDict[tmpCarName][tmpSysName]:
					if isinstance(retDict[tmpCarName][tmpSysName][tmpEcuName], list) :
						retDict[tmpCarName][tmpSysName][tmpEcuName].append(tmpEcuId)
					else:
						print("error")
				continue
			else:
				pass
	return retDict



def GetKAddr(inKwpEnterCmd):
	'''
	:param inKwpEnterCmd: kwp系统进入命令
	:return: k地址
	'''
	#8101F381F6
	if len(inKwpEnterCmd) == 0:
		return "?"
		#raise ValueError

	return  inKwpEnterCmd[4:5+1] +  inKwpEnterCmd[2:3+1]   #返回 F301


def GetCanEcuAddr(inCanEnterCmd):
	'''
	:param inCanEnterCmd:  can协议系统进入命令
	:return: Can协议的ecu地址
	'''
	#07C5021081
	if len(inCanEnterCmd) == 0:
		return  "?"
		#raise ValueError
	return inCanEnterCmd[ : 4] #07C5

def GetCanToolAddr(inCanReplyCmd):
	'''
	:param inCanReplyCmd: can协议系统进入命令的回复
	:return: Tool地址
	'''
	#07CD5081
	if len(inCanReplyCmd) == 0:
		return "?"
		#raise ValueError
	return inCanReplyCmd[ : 4]   #07CD



def	ReadEcuParam(carName, sysName, ecuName, eachEcuId, outFile):
	'''
	:param inEcuId:  读取ecu相关信息
	:return: 无
	'''

	#这种方式效率低,但是此处运行效率不在考虑范围内
	tt = TextTool("../doc/tmp/out_Ecu_Info.txt")


	outFile.write("{0}\t{1}\t{2}\t{3}\t".format(carName, sysName, ecuName, eachEcuId))

	ecuId = eachEcuId
	allSectDict = tt.allSectDictOfFile
	tmpIndex = "0xFF,0xFF,0xFF,0xFF,0xFF," + MyHex(ecuId[-2:])

	for fieldName, filedDict in allSectDict[tmpIndex].items(): #就一个["Netlayer"]而已

		#协议名
		if filedDict["ProtocolName"][0] == "":
			outFile.write("{0}\t".format(" "))
		else:
			outFile.write("{0}\t".format(filedDict["ProtocolName"][0]))

		#波特率
		if filedDict["BauteRate"][0] == "":
			outFile.write("{0}\t".format(" "))
		else:
			if filedDict["ProtocolName"][0] == "CAN":
				outFile.write("{0}\t".format("500k"))
			else:
				outFile.write("{0}\t".format(filedDict["BauteRate"][0]))


		# 引脚
		#if filedDict["ProtocolName"][0] == "KWP2000":
		#KWP2000, KWP2000(5bps), KWP_0x 三种KWP协议的都可以计算引脚
		if "KWP" in filedDict["ProtocolName"][0]:
			#outFile.write("{0}\t".format("7"))
			outFile.write("{0},{0}\t".format(CalcComPin(filedDict["ComPin"][0])))

			outFile.write("{0}\t".format(GetKAddr(filedDict["EnterCmd"][0]))) #k地址
			outFile.write("{0}\t".format("   ")) #CanEcu地址,留白
			outFile.write("{0}\t".format("   ")) #CanTool地址,留白
		elif filedDict["ProtocolName"][0] == "CAN":
			outFile.write("{0}\t".format("6,14"))

			outFile.write("{0}\t".format(" ")) #k地址, 留白
			outFile.write("{0}\t".format(GetCanEcuAddr(filedDict["EnterCmd"][0]))) #CanEcu地址
			outFile.write("{0}\t".format(GetCanToolAddr(filedDict["EnterReply"][0]))) #CanTool地址
		else:
			outFile.write("{0}\t".format("  "))
			outFile.write("{0}\t".format("  "))
			outFile.write("{0}\t".format("  "))

		#outFile.write("{0}\t".format("?")) #k地址
		#outFile.write("{0}\t".format("?")) #CanEcu地址
		#outFile.write("{0}\t".format("?")) #CanTool地址


		if "EnterCmd" in filedDict:
			if filedDict["EnterCmd"][0] == "":
				outFile.write("{0}\t".format(" ")) #进入系统命令
			else:
				outFile.write("{0}\t".format(filedDict["EnterCmd"][0])) #进入系统命令
		else:
			print("no enter cmd")
		outFile.write("{0}\t".format("?")) #进系统掩码
		outFile.write("{0}\t".format("?")) #停止会话命令

		if "KeepLinkCmd" in filedDict:
			if filedDict["KeepLinkCmd"][0] == "":
				outFile.write("{0}".format(" ") )#链路命令为空, 填个空格符
			else:
				outFile.write("{0}".format(filedDict["KeepLinkCmd"][0])) #链路命令

		outFile.write("\n")
	pass


def ReadMenuDict(inDict, outFile):
	'''
	Recursion for the god, Iteration for me.
	:param inDict:  输入的菜单树
	:param outFile:  输出文件 
	:return: 无
	'''

	for carName, carDict in inDict.items():
		for sysName , ecuDict in carDict.items():
			for ecuName, ecuIdList in ecuDict.items():
				for eachEcuId in ecuIdList:
					ReadEcuParam(carName, sysName, ecuName, eachEcuId, outFile)
	pass



def main():
	
	retDict = ReadRootMenuFile("../txt/CN_ROOT.txt")

	outFile = open("../doc/tmp/out_Ecu_Table.txt", "w")
	ReadMenuDict(retDict, outFile)
	outFile.close()

	print(len(retDict))
	for key, value in retDict.items():
		print("{0} = {1}".format(key, value))


	pass


if __name__ == "__main__":

	main()

	pass