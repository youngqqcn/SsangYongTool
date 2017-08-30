#!coding:utf8

'''
Date:2017/8/14/19:55
Author:yqq
Description:none
'''

from collections import OrderedDict
#from lib.mytool6 import TabTextTool
from lib.mytool7 import TabTextTool
#from lib.mytool6 import MyHex
from lib.mytool7 import MyHexPlus

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

def MyCounter(tt):
	'''
	统计????5的种类与个数
	:return: 
	'''

	counterDict = {}
	for eachLineDict in tt.allNamedSplitedList:
		if "????5" in eachLineDict:
			if eachLineDict["????5"] not in counterDict:
				counterDict[eachLineDict["????5"]] = 1
			else:
				counterDict[eachLineDict["????5"]] += 1

	print(len(counterDict))

	print("==================")
	counterDict = OrderedDict(sorted(counterDict.items(), key=lambda item: item[0]))
	sum = 0
	for name, count in counterDict.items():
		print("{0}={1}\n".format(name, count))
		sum += count
	print("=============\nsum={0}".format(sum))

	pass


def MyCounter2(tt):
	'''
	:param tt:  模式33的是个数
	:return: 
	'''
	iCounter = 0
	for eachLineDict in tt.allNamedSplitedList:
		if "k1" in eachLineDict:
			if eachLineDict["DsMode"] == "33":
				iCounter += 1
				if eachLineDict["k1"] != "6":
					print(eachLineDict["NO"])
	print("====\n{0}".format(iCounter))

	pass



def MyCounter3(tt):
	'''
	计算模式65的EcuID
	:return: 
	'''
	iCounter = 0
	tmpList = []
	for eachLineDict in tt.allNamedSplitedList:
		if "DsMode" in eachLineDict:
			if eachLineDict["DsMode"] == "65":
				if eachLineDict["EcuID"] not in tmpList:
					if int(eachLineDict["EcuID"], 10) <= 900010:
						pass
						#continue
					tmpList.append(eachLineDict["EcuID"])
				iCounter += 1
	print("====\n{0}".format(iCounter))

	print("============")
	for item in tmpList:
		print(item)

	pass


def MyPrintMode33(tt):

	'''
	把模式33的数据流相关信息输出到一个文件中
	:return: 
	'''

	iCount = 0
	outFile = open("../doc/tmp/Mode33.txt", "w")
	for eachLineDict in tt.allNamedSplitedList:
		if int(eachLineDict["EcuID"], 10) <= 900010:
			continue
		if eachLineDict["DsMode"] == "33":
			iCount += 1

			print("\n==========")
			outFile.write("\n==========\n")

			print("NO={0}".format(eachLineDict["NO"]))
			outFile.write("NO={0}\n".format(eachLineDict["NO"]))

			print("EcuID={0}".format(eachLineDict["EcuID"]))
			outFile.write("EcuID={0}\n".format(eachLineDict["EcuID"]))

			print("DsName={0}".format(eachLineDict["DsName"]))
			outFile.write("DsName={0}\n".format(eachLineDict["DsName"]))

			print("DsCmd={0}".format(eachLineDict["DsCmd"]))
			outFile.write("DsCmd={0}\n".format(eachLineDict["DsCmd"]))

			print("CtrlByte={0}".format(eachLineDict["CtrlByte"]))
			outFile.write("CtrlByte={0}\n".format(eachLineDict["CtrlByte"]))

			print("k1={0}".format(eachLineDict["k1"]))
			outFile.write("k1={0}\n".format(eachLineDict["k1"]))

			print("k2={0}".format(eachLineDict["k2"]))
			outFile.write("k2={0}\n".format(eachLineDict["k2"]))

			print("k3={0}".format(eachLineDict["k3"]))
			outFile.write("k3={0}\n".format(eachLineDict["k3"]))

			print("k4={0}".format(eachLineDict["k4"]))
			outFile.write("k4={0}\n".format(eachLineDict["k4"]))
	outFile.close()

	print("=======\n{0}".format(iCount))
	pass


def MyCounter4(tt):

	'''
	:param tt:  统计模式33, k3和k4的种类
	:return: 
	'''
	iCounter = 0

	outFile = open("../doc/tmp/CountMode33.txt", "w")


	tmpList = []
	for eachLineDict in tt.allNamedSplitedList:
		#if int(eachLineDict["NO"] , 10) <= 900010:
		#	continue
		if "DsMode" in eachLineDict:
			if eachLineDict["DsMode"] == "33":
				tmpStr = eachLineDict["k3"] + ";" + eachLineDict["k4"]
				if tmpStr not in tmpList:
					print("{0}-->{1}-->{2}".format(tmpStr, eachLineDict["EcuID"], eachLineDict["NO"]))
					outFile.write("{0}\t{1}\t{2}\n".format(tmpStr, eachLineDict["EcuID"], eachLineDict["NO"]))
					tmpList.append(tmpStr)




	#print(len(tmpList))
	#print("===========")

	#for item in tmpList:
	#	print(item)
	if isinstance(outFile, file):
		print("close file")
		outFile.close()
	pass






'''
	def WriteFile(self, outFilePath):

		tmpList = self.allNamedSplitedList

		if len(tmpList) == 0:
			raise ValueError
		else:
			with open(outFilePath, "w") as outFile:
				for eachLine in tmpList:
					outFile.write("\n=============\n")
					for eachFieldName, eachFieldValue in eachLine.items():
						if "NO-USE" in eachFieldName: continue
						outFile.write("\t{0}={1}\n".format(
							eachFieldName, eachFieldValue
						))

'''


def WriteFile(allNamedSplitedList, outFile):
	'''
	:param allNamedSplitedList:  重写WriteFile函数, 以公司支持的格式写入
	:return: 无
	'''
	tmpList = allNamedSplitedList
	if len(tmpList) == 0:
		raise ValueError
	else:
		for eachLine in tmpList:
			if int(eachLine["EcuID"].strip(), 10) <= 900010:  #匹配没有开发的
				continue
			outFile.write("0xFF,0xFF,0xFF,0xFF,{0}\t\t\\\"\n".format(MyHexPlus(eachLine["NO"])))
			outFile.write("[Netlayer]\t\t\t\t\t\\n\\\n")
			for key, value in eachLine.items():
				if "NO-USE" in key: continue
				outFile.write("\t{0}={1}\t\t\t\t\t\\n\\\n".format(key.strip(), value.strip()))
			outFile.write("\t\t\t\t\t\\n\"\n\n")

	pass



def main():

	tt = TabTextTool("../txt/DS_Info.txt", gFieldNameList)
	#tt.ShowAll()

	#[{field1: value1, filed2: value2, ....}, {}, {}, ....]
	#统计一下   ????5有多少种, 每种有多少个
	#MyCounter2(tt)
	#MyPrintMode33(tt)
	#MyCounter3(tt)
	#MyCounter4(tt)



	#使用类的方法, 写文件
	#tt.WriteFile("../doc/tmp/out_DS_Info.txt" )
	#tt.allNamedSplitedList

	#使用自定义方法, 写文件
	with open("../doc/tmp/out_DS_Info2.txt", "w") as outFile:
		WriteFile(tt.allNamedSplitedList, outFile )


	pass


if __name__ == "__main__":

	main()

	pass