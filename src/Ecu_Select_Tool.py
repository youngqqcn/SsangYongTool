#!coding:utf8

'''
Date:2017/8/14/11:01
Author:yqq
Description:提取root菜单
'''

from collections import OrderedDict
from lib.mytool6 import TabTextTool
from lib.mytool6 import MyHex
from lib.mytool6 import ReadText


gFieldKeyNameList = [
	"No",
	"????0",
	"CarNameID",
	"SysNameID",
	"SubSysNameID",
	"EcuID",
	"????1",
]

gRetDict = ReadText("../txt/cn_text.txt")



def GetCarName(inCarNameIndex):
	'''
	:param inCarNameIndex: 车型名称的索引
	:return: 车型名称
	'''

	#retDict = ReadText("../txt/cn_text.txt")
	index = "0x55,0x43,0x48,0x01,0x00," + MyHex(inCarNameIndex)
	return gRetDict[index]


def GetSysName(inSysNameIndex):
	'''
	:param inSysNameIndex:获取系统名 
	:return: 
	'''

	#retDict = ReadText("../txt/cn_text.txt")
	index = "0x55,0x43,0x48,0x02,0x00," + MyHex(inSysNameIndex)
	return gRetDict[index]


def GetEcuName(inEcuNameIndex):
	'''
	:param inEcuNameIndex: 在文本库中获取ecu名称
	:return: 
	'''
	#retDict = ReadText("../txt/cn_text.txt")
	index = "0x55,0x43,0x48,0x03,0x00," + MyHex(inEcuNameIndex)
	return gRetDict[index]




def WriteFile(outFile, inDict):
	'''
	:param outFile:  输出的ROOT菜单 
	:param inDict:  菜单字典
	:return: 无 
	
	数据结构: 
			myDict{
				careId{ //车型
					SysId{//系统
						EcuName1 : [EcuId1], 
						EcuName2 : [EcuId1, EcuId2, EcuId3,...], #存在一个多个ecuId对应同一个名字
						...
					}
				}
			}

	'''

	if(isinstance(inDict, dict)):
		for carName in inDict:
			#print("\t{0}\n".format(carName))
			outFile.write("\t{0}\n".format(GetCarName(carName)))
			for sysName in inDict[carName]:
				#print("\t\t{0}\n".format(sysName))

				#如果只有1个子系统, 没有必要再分下一级菜单
				if len(inDict[carName][sysName]) == 1:
					if len(inDict[carName][sysName].items()[0][1]) > 1:
						#特殊情况: 一个系统下只有一个ecu, 一个ecu名由多个ecuId; 这种情况在此并不存在
						print("special")
						raise KeyError

					outFile.write("\t\t{0}<{1}>\n".format(
						GetSysName(sysName), inDict[carName][sysName].items()[0][1][0]
					))
					continue
				else:
					outFile.write("\t\t{0}\n".format(GetSysName(sysName)))
					for subName, ecuIdList in inDict[carName][sysName].items():
						'''
						print("\t\t\t{0}<{1}>\n".format(
							subSysAndEcuIdDict.keys()[0],
							subSysAndEcuIdDict.values()[0]
						))
						'''
						if len(ecuIdList) > 1:  #如果有多个ecu同名
							outFile.write("\t\t\t{0}\n".format(GetEcuName(subName)))
							for i in range(len(ecuIdList)):
								outFile.write("\t\t\t\t{0}<{1}>\n".format(GetEcuName(subName) + str(i+1), ecuIdList[i] ))
						else:
							outFile.write("\t\t\t{0}<{1}>\n".format(GetEcuName(subName), ecuIdList[0]))

				pass #for
			pass #for
	else: #inDict is not dict object
		raise ValueError
	pass




def main():
	'''
	数据结构: 
		myDict{
			careId{ //车型
				SysId{//系统
					EcuName1 : [EcuId1], 
					EcuName2 : [EcuId1, EcuId2, EcuId3,...], #存在一个多个ecuId对应同一个名字
					...
				}
			}
		}
	
	'''

	tt = TabTextTool("../txt/Ecu_Select.txt", gFieldKeyNameList)

	outFile = open("../doc/tmp/out_Ecu_Select.txt", "w")
	outFile.write("out_SsangYong\n")

	myDict = OrderedDict()

	for lineDict in tt.allNamedSplitedList:
		if lineDict["CarNameID"] not in myDict:
			myDict[lineDict["CarNameID"]] = OrderedDict()
		if lineDict["SysNameID"] not in myDict[lineDict["CarNameID"]]:
			myDict[lineDict["CarNameID"]][lineDict["SysNameID"]] = OrderedDict()
		if lineDict["SubSysNameID"] not in myDict[lineDict["CarNameID"]][lineDict["SysNameID"]]:
			myDict[lineDict["CarNameID"]][lineDict["SysNameID"]][lineDict["SubSysNameID"]] = []
		myDict[lineDict["CarNameID"]][lineDict["SysNameID"]][lineDict["SubSysNameID"]].append(lineDict["EcuID"] )


	#print(len(myDict))
	WriteFile(outFile, myDict)

	outFile.close()

	pass


if __name__ == "__main__":

	main()

	pass