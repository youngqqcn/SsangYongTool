#! coding:utf8
import re
import os

'''
段(section): 从段ID加上'\"'开始到'\n"'结束

域(filed):  如: "[Menu]"

键值对(keyPair): 如: 'VehEcuID=1389'

'''
# 数据结构:
# dict = {sect1:{filed1:{key1:[value1, value2], key2:[value1, value2]}}}

from collections import OrderedDict


class TextTool:
	def __init__(self, filePath, isOrder=True):

		self.__filePath = filePath
		self.allSectListOfFile = []

		# 设置是否按照插入的顺序排序
		self.__isOrder = isOrder
		if self.__isOrder:
			self.allSectDictOfFile = OrderedDict()
		else:
			self.allSectDictOfFile = {}

		self.GetAllSectDictFromFile()
		pass

	def GetFieldsFromSect(self, sectString):

		lineList = sectString.splitlines()
		sectHexStrID = (lineList[0].strip())[0: lineList[0].find('\t')]
		filedList = sectString.split('[')

		if self.__isOrder:
			sectFiledsDict = OrderedDict()
		else:
			sectFiledsDict = {}

		for filed in filedList:
			filedLineList = filed.splitlines()
			filedName = ''

			if self.__isOrder:
				filedKVDict = OrderedDict()
			else:
				filedKVDict = {}

			for line in filedLineList:
				if '=' in line:
					key = line.split('=')[0].strip()
					tmpKeyList = key.split('+')
					tmpValue = line.split('=')[1]
					value = tmpValue[0: tmpValue.find('\t')]
					for eachKey in tmpKeyList:
						if eachKey not in filedKVDict:
							filedKVDict[eachKey] = []
						filedKVDict[eachKey].append(value)
					continue
				if ']' in line:
					filedName = line[0: line.find(']')]
			if filedName != '':
				sectFiledsDict[filedName] = filedKVDict
		self.allSectDictOfFile[sectHexStrID] = sectFiledsDict
		pass

	def GetAllSectDictFromFile(self):

		with open(self.__filePath, 'r') as f:
			fileContent = f.read()

		pattern = r'^0x.*?\\n\"'  # 用正则表达式匹配" 段"
		reObj = re.compile(pattern, re.DOTALL + re.MULTILINE)
		self.allSectListOfFile = reObj.findall(fileContent)

		for sect in self.allSectListOfFile:
			self.GetFieldsFromSect(sect)
			pass

	def ShowAll(self):

		allSectDict = self.allSectDictOfFile
		for sectKey in allSectDict:
			sectDict = allSectDict[sectKey]
			print ('{0}'.format(sectKey))
			for filedKey in sectDict:
				filedDict = sectDict[filedKey]
				print ('[{0}]'.format(filedKey))
				for keyPairKey in filedDict:
					for listItem in filedDict[keyPairKey]:
						print('{0}={1}'.format(keyPairKey, listItem))
				print ('\n')
		pass


class TabTextTool:
	'''
	处理制表符分隔的文件类
	数据结构: 一行一个列表
	'''

	class LengthNotMatchError(RuntimeError):
		def __init__(self, arg):
			# print(arg)
			self.message = "Length Not Matching!"
			self.args = arg

	def __init__(self, inFilePath, inFieldNameList=list()):
		self.inFilePath = inFilePath
		self.allSplitedLineList = self.ReadTabFile(inFilePath)
		self.allNamedSplitedList = []
		if len(inFieldNameList) > 0:
			self.allNamedSplitedList = self.AddFieldName(self.allSplitedLineList, inFieldNameList)

	def ReadTabFile(self, inFilePath):
		retList = []
		if os.path.isfile(inFilePath):
			with open(inFilePath, "r") as inFile:
				contentList = inFile.readlines()
				for eachLine in contentList:
					if '\t' in eachLine:
						tmpSplitedList = eachLine.split("\t")
						if len(tmpSplitedList) != 0:
							retList.append(tmpSplitedList)
						else:
							retList.append([])
				pass
		return retList


	def AddFieldName(self, allSplitedLineList, inFieldNameList):
		'''
		:param allSplitedLineList:  
		:param inFieldNameList: 数据结构 : [{field1:value1, filed2:value2, ....}, {}, {},....]
		:return: 
		'''

		retList = []

		for eachLine in allSplitedLineList:

			if len(eachLine) != len(inFieldNameList):
				# 引发一个自定义异常
				print(len(eachLine))
				print(len(inFieldNameList))
				raise self.LengthNotMatchError(inFieldNameList)

			tmpLineDict = OrderedDict()
			for i in range(len(eachLine)):
				tmpLineDict[inFieldNameList[i]] = eachLine[i]
			retList.append(tmpLineDict)
		return retList



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
		pass



	def ShowAll(self):
		inList = self.allSplitedLineList
		for eachLine in inList:
			print("\n==============")
			for eachField in eachLine:
				print("{0}={1}\n".format("????", eachField))




def ReadText(inFilePath):
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
				value = tmpStr[tmpStr.find("\"") + 1: tmpStr.rfind("\"")].strip()
				retLanDict[key] = value
		return retLanDict


def Add0x(inStr):
	'''
	:param inStr: 例如:   0022334455    
	:return: 返回 0x00,0x22,0x33,0x44,0x55
	'''
	inStr = inStr.strip()
	if (len(inStr) & 1):  # 输入的是奇数
		print(">>>>"+inStr)
		raise ValueError
	else:
		return ''.join("0x" + inStr[i * 2: i * 2 + 2] + "," for i in range(len(inStr) / 2))[0: -1]
	pass


def Del0x(inStr):
	'''
	:param inStr:0x00,0x22,0x33,0x44,0x55 
	:return:0022334455   
	'''
	return inStr.replace("0x", "").replace(",", "")


def MyHex(inArg):
	'''
	:param inArg:  
	:return: 将一个整数(最大255), 或者十进制整数字符串转换为0xAB类型的
	'''

	tmpStr = str(inArg)
	if tmpStr.isdigit():
		tmpInt = int(tmpStr, 10)
		if tmpInt > 255:
			raise ValueError
	else:
		print(type(inArg))
		raise ValueError
	return "0x" + ("%02x" % tmpInt).upper()
