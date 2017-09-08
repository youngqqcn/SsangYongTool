#!coding:utf8

'''
Date:2017/8/15/20:04
Author:yqq
Description:
	从原文本库中提取, 放在一个文件中, 文件名为EcuID: 
		1.版本信息(数据或算法); 
		2.故障码数据; 
		3.数据流数据.
'''

from collections import OrderedDict
from lib.mytool6 import *



gVerInfoFilePath = "../txt/System_Info.txt"
gDtcFilePath = "../txt/Ecu_Dtc.txt"
gDsFilPath = "../txt/DS_Info.txt"


gVerInfoFieldNameList = [
		"No",
		"???1",
		"EcuId",
		"???2",
		"VerCmd",
		"VerReply",
		"VerExp"
]

gDtcFiledNameList = [
		"No",
		"???1",
		"EcuId",
		"DtcNo",
		"OtherNo",
]

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
		"????6",  # ???
		"????7"  # 无用
]



#数据结构 : [{field1:value1, filed2:value2, ....}, {}, {},....]

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


def WriteData(inVerDict, inDtcDict, inDsDict):
	'''
	:param inVerDict: 版本信息数据
	:param inDtcDict: 故障码数据
	:param inDsDict: 数据流数据
	:return:无 
	'''

	#数据结构: {
	#			 EcuId1:[
	#                       #Info1#  {field1:value1, field2:value2,...},
	#						#Info2# {...},
	#                       #Info3# {...}
	#                           ...
	#					],
	#			 EcuId2:[
	#                       #Info1# ...
	#                       #Info2# ...
	#                       #Info3# ...
	#                        ...
	#                   ],
	#            EcuId3:[
	#                       ...
	#                   ],
	#            ...
	#         }

	for intEcuID in range(900011, 900061+1):

		if intEcuID in [900025, 900026, 900027]:
			continue

		ecuId = str(intEcuID)
		with open("../doc/out_SsangYong/"+ ecuId + ".txt", "w") as outFile:

			#写入版本信息数据
			outFile.write("0xFF,0xFF,0xFF,0xFF,0xFF,0x00\t\t\"\\\n")
			outFile.write("[Data]\t\t\t\t\t\\n\\\n")
			if ecuId in inVerDict:
				iCount = 0
				outFile.write("\tInfoNum={0}\t\t\\n\\\n".format(len(inVerDict[ecuId]))) #版本信息命令条数
				for eachInfoDict in inVerDict[ecuId]:
					outFile.write("\tInfo{0}=".format(iCount))
					outFile.write("{0},{1},{2},{3}\t\t\\n\\\n".format(
						eachInfoDict["???2"], eachInfoDict["VerCmd"],
						eachInfoDict["VerReply"],
						#eachInfoDict["VerExp"][0:-2] #去掉版本信息算法的换行符
						eachInfoDict["VerExp"].replace("\r\n", "")#去掉版本信息算法的换行符
					))
					iCount += 1
				pass
			else:
				outFile.write("\tInfoNum=0\t\t\\n\\\n") #没有
				pass
			outFile.write("\t\t\t\t\t\\n\"\n\n") #版本信息数据结尾


			#写入故障码数据
			outFile.write("0xFF,0xFF,0xFF,0xFF,0xFF,0x01\t\t\"\\\n")
			outFile.write("[Data]\t\t\t\t\t\\n\\\n")
			if ecuId in inDtcDict:
				iCount = 0
				outFile.write("\tDtcNum={0}\t\t\\n\\\n".format(len(inDtcDict[ecuId]))) #故障码条数
				for eachDtcDict in inDtcDict[ecuId]:
					outFile.write("\tDtc{0}=".format(iCount))
					outFile.write("{0},{1}\t\t\\n\\\n".format(
						eachDtcDict["DtcNo"].strip(), eachDtcDict["OtherNo"].strip()
					))
					iCount += 1
			else:
				outFile.write("\tDtcNum=0\t\t\\n\\\n")
			outFile.write("\t\t\t\t\t\\n\"\n\n")  #故障码数据结尾


			#写入数据流数据

			# 	'''
			# "DsName",
			# "DsCmd",
			# "Reply",
			# "CtrlByte",
			# "Length",
			# "k1",
			# "k2",
			# "k3",  # ??
			# "k4",  # ??
			# "DsMode",
			# "????4",  # ???
			# "????5",  # ???
			# "????6",  # ???
			# "????7"  # 无用
			#
			# 	'''

			outFile.write("0xFF,0xFF,0xFF,0xFF,0xFF,0x02\t\t\"\\\n")
			outFile.write("[Data]\t\t\t\t\t\\n\\\n")
			if ecuId in inDsDict:
				iCount = 0
				outFile.write("\tDsNum={0}\t\t\\n\\\n".format(len(inDsDict[ecuId]))) #故障码条数
				for eachDsDict in inDsDict[ecuId]:
					outFile.write("\tDs{0}=".format(iCount))
					outFile.write("{0},{1},{2},{3},{4},{5},{6}\t\t\\n\\\n".format(
						eachDsDict["NO"], eachDsDict["DsName"], eachDsDict["DsCmd"],
						eachDsDict["Reply"], eachDsDict["CtrlByte"], eachDsDict["Length"],
						eachDsDict["DsMode"],
					))
					iCount += 1
			else:
				outFile.write("\tDsNum=0\t\t\\n\\\n")
			outFile.write("\t\t\t\t\t\\n\"\n\n")  #数据流数据结尾

	pass



def main():

	#获取版本信息数据
	infoDict = ReadData(gVerInfoFilePath, gVerInfoFieldNameList)
	#print(len(infoDict))

	#获取故障码数据
	dtcDict = ReadData(gDtcFilePath, gDtcFiledNameList)
	#print(len(dtcDict))

	#获取数据流数据
	dsDict = ReadData(gDsFilPath, gDsFieldNameList)
	#print(len(dsDict))

	#写入文件
	WriteData(infoDict, dtcDict, dsDict)

	pass


if __name__ == "__main__":

	main()

	pass