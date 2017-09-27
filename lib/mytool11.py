#! coding:utf8

# version 11 , update time: 2017/9/26
# update description :
#    在TabTextTool中增加了文件是否存在的判断,如果文件不存在,则引发异常



import re
import os
from collections import OrderedDict   #有序字典




class TextTool:

	'''
	# TextTool说明:
	# 段(section): 从段ID加上'\"'开始到'\n"'结束 
	# 域(filed):  如: "[Menu]"
	# 键值对(keyPair): 如: 'VehEcuID=1389'

	# 数据结构:
	# dict = {sect1:{filed1:{key1:[value1, value2], key2:[value1, value2]}}}	

	'''

	def __init__(self, filePath, isOrder=True):
		'''
		:param filePath: 输入文件路径
		:param isOrder: 是否有序, True:有序(速度慢); False: 无序(速度快)
		'''

		self.__filePath = filePath.strip()
		self.allSectListOfFile = []

		# 设置是否按照插入的顺序排序
		self.__isOrder = isOrder
		if self.__isOrder:
			self.allSectDictOfFile = OrderedDict()
		else:
			self.allSectDictOfFile = {}

		self.__GetAllSectDictFromFile()
		pass

	def __GetFieldsFromSect(self, sectString):
		'''
		:param sectString: 
		:return: 
		'''

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

	def __GetAllSectDictFromFile(self):
		'''
		:return: 
		读数据
		'''

		with open(self.__filePath, 'r') as f:
			fileContent = f.read()

		pattern = r'^0x.*?\\n\"'  # 用正则表达式匹配" 段"
		reObj = re.compile(pattern, re.DOTALL + re.MULTILINE)
		self.allSectListOfFile = reObj.findall(fileContent)

		for sect in self.allSectListOfFile:
			self.__GetFieldsFromSect(sect)
			pass

	def ShowAll(self):
		'''
		:return: 无
		打印
		'''

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

	def WriteFile(self, filePath ):
		'''
		此方法主要用于, 修改值之后, 写回文件
		:param filePath: 输出文件路径
		:return: 
		'''

		#if not os.path.exists(os.path.dirname(filePath)):
		#	os.mkdir(os.path.dirname(filePath)) #如果目录不存在则创建

		if self.__filePath.strip() == filePath.strip():
			print("inFile == outFile")  # 输入的文件和输出的文件不能是同一个
			raise ValueError

		if os.path.exists(os.path.dirname(filePath)):
			with open(filePath, "w") as outFile:
				allSectDict = self.allSectDictOfFile
				for sectKey in allSectDict:
					sectDict = allSectDict[sectKey]
					#print ('{0}'.format(sectKey))
					outFile.write('{0}\t\t\"\\\n'.format(sectKey))  #索引
					for filedKey in sectDict:
						suffix = '\t'*5 + '\\n\\\n'
						filedDict = sectDict[filedKey]
						#print ('[{0}]'.format(filedKey))
						outFile.write('[{0}]{1}'.format(filedKey, suffix)) #域名
						for keyPairKey in filedDict:
							for listItem in filedDict[keyPairKey]:
								#print('{0}={1}'.format(keyPairKey, listItem))
								outFile.write('\t{0}={1}{2}'.format(keyPairKey, listItem, suffix)) #键值对
					outFile.write("{0}".format('\t'*5 + '\\n\"\n\n'))
			pass
		else:
			print("Dir not exist!")
			raise ValueError


class TabTextTool:
	'''
	#处理以tab键分隔的文件
	#处理制表符分隔的文件类
	#数据结构: 一行一个列表
	[{k1:v1, k2:v2, k3:v3}, {k1:v1, k2:v2, ...}, {},... ]
	'''

	class LengthNotMatchError(RuntimeError):
		'''
		自定义一个异常类
		'''
		def __init__(self, arg):
			# print(arg)
			self.message = "Length Not Matching!"
			self.args = arg

	def __init__(self, inFilePath, inFieldNameList=list()):
		self.inFilePath = inFilePath
		self.allSplitedLineList = self.__ReadTabFile(inFilePath)
		self.allNamedSplitedList = []
		if len(inFieldNameList) > 0:
			self.allNamedSplitedList = self.__AddFieldName(self.allSplitedLineList, inFieldNameList)

	def __ReadTabFile(self, inFilePath):
		'''
		:param inFilePath: 输入文件路径
		:return: 
		'''
		retList = []
		if not os.path.exists(inFilePath):  #文件不存在, 引发异常
			print("inFilePath not exists")
			raise ValueError
		if os.path.isfile(inFilePath):
			with open(inFilePath, "r") as inFile:
				contentList = inFile.readlines()
				for eachLine in contentList:
					if '\t' in eachLine:
						tmpListSplitedList = []
						tmpList = eachLine.split("\t")
						if len(tmpList) != 0:
							for item in tmpList:
								tmpListSplitedList.append(item.strip())
							retList.append(tmpListSplitedList)
						else:
							retList.append([])
				pass
		return retList


	def __AddFieldName(self, allSplitedLineList, inFieldNameList):
		'''
		:param allSplitedLineList:  
		:param inFieldNameList: 
		数据结构 : [{field1:value1, filed2:value2, ....}, {}, {},....]
		:return: 
		'''

		retList = []

		for eachLine in allSplitedLineList:

			if len(eachLine) != len(inFieldNameList):
				# 引发一个自定义异常
				print(len(eachLine))
				print(len(inFieldNameList))
				raise self.LengthNotMatchError(inFieldNameList)   #key的数量和value的数量不匹配,异常

			tmpLineDict = OrderedDict()
			for i in range(len(eachLine)):
				tmpLineDict[inFieldNameList[i]] = eachLine[i]
			retList.append(tmpLineDict)
		return retList



	def WriteFile(self, outFilePath):
		'''
		:param outFilePath: 输出文件路径
		:return: 
		如果需自定义输出文件格式, 重写这个函数即可
		'''

		tmpList = self.allNamedSplitedList

		if len(tmpList) == 0:
			raise ValueError
		else:
			with open(outFilePath, "w") as outFile:
				for eachLine in tmpList:
					outFile.write("\n=============\n")
					for eachFieldName, eachFieldValue in eachLine.items():
						if "NO-USE" in eachFieldName: continue
						outFile.write("\t{0}={1}\n".format(eachFieldName, eachFieldValue))
		pass



	def ShowAll(self):
		inList = self.allSplitedLineList
		for eachLine in inList:
			print("\n==============")
			for eachField in eachLine:
				print("{0}={1}\n".format("????", eachField))




class RootMenu:
	'''
	RootMenu说明: 使用此类时, root菜单文件的首行必须是"车名", 
	             如果有多个"车"(不是车型), 则只要把
	             __init__函数中, lineList.remove(lineList[0]) 注释掉即可
	'''

	def __init__(self, inFilePath, isOrder=True):
		if os.path.isfile(inFilePath):
			with open(inFilePath, "r") as inFile:
				lineList = inFile.readlines()

				#lineList.remove(lineList[0]) #去掉首行的车名, 如果有多个车(不是车型, 如: 高低配),注释这句即可

				self.__isOrder = isOrder  #True表示按照插入顺序排序(速度慢), False则为无序(速度快)
				if self.__isOrder:
					self.menuDict= OrderedDict()    #菜单树,(有序)
				else:
					self.menuDict= {}    #菜单树,(无序)
				self.__AddMenuItem(self.menuDict, lineList)
				# print(len(retDict))
				#ShowAll(retDict, 0)
				pass
		else:
			raise ValueError
		pass

	def __AddMenuItem(self, inDict, nodeList):
		'''
		:param inDict: 传入传出参数, 菜单树(字典)
		:param nodeList: 剩余的节点列表
		:return: 无
		'''

		# 算法设计(递归)
		# 1.如果是叶子节点,将此节点挂在其父节点下面; --->递归边界条件
		# 2.如果不是叶子节点,将此节点的所有子节点挂上来, 再把此节点挂在其父节点上;
		# 3.再处理其他节点

		if (nodeList == None) | (nodeList == []):
			return
		if self.__IsLeafNode(nodeList[0]):  # 1.如果是叶子节点, 将此节点挂在其父节点下面; --->递归边界条件
			inDict[self.__GetLeafNodeNameAndID(nodeList[0])[0]] = [self.__GetLeafNodeNameAndID(nodeList[0])[1]]
			nodeList.remove(nodeList[0])
		else:
			if self.__isOrder:
				tmpDict = OrderedDict()  #有序字典
			else:
				tmpDict = {} #无序字典

			tmpNode = nodeList[0]
			subNodeList = self.__GetSubNode(nodeList)

			self.__AddMenuItem(tmpDict, subNodeList)  # 2.将此节点下的所有子节点挂上来
			inDict[tmpNode.strip()] = tmpDict  # 再把此节点挂在其父节点上

		self.__AddMenuItem(inDict, nodeList)  # 3.再处理其他的节点

		pass

	def __GetSubNode(self, inList):
		'''
		:param inList: 剩余节点链表(还未处理的节点列表)
		:return: inList[0] 下所有子节点组成的列表, 所有这些处理过的子节点都会从inList中永久删除
		'''

		# 获取此节点下所有子节点,同时删掉以处理掉的节点
		parentNode = inList[0]  # 将第一个作为父节点
		inList.remove(inList[0])  # 永久删除已经处理的parentNode这个节点,注意remove()是没有返回值
		if len(inList) == 0:
			return []

		tmpNodeList = []
		while True:
			if len(inList) == 0:  # 节点列表空了
				break
			if inList[0].count('\t') > parentNode.count('\t'):  # 即字节点的tab的数量一定大于父节点
				tmpNodeList.append(inList[0])
				inList.remove(inList[0])  # 删掉已经处理过的节点
			else:
				break
		return tmpNodeList

	def __IsLeafNode(self, inStr):
		'''
		:param inStr: 节点字符串
		:return: 如果是叶子节点返回True; 否则返回False
		'''
		inStr = inStr.strip()
		if ('<' in inStr) & ('>' in inStr):
			return True
		return False

	def __GetLeafNodeNameAndID(self, inStr):
		'''
		:param inStr: 节点字符串, 比如:   安全气囊<900021> 
		:return: 返回节点名称(Ecu名称)和节点ID(ECU ID)
		'''

		inStr = inStr.strip()
		if ('<' in inStr) & ('>' in inStr):
			return [inStr[: inStr.find('<')], inStr[inStr.find('<') + 1: inStr.find('>')]]
		raise ValueError

	def ShowAll(self, inDict = 'self.menuDict', tabCount = 0):
		'''
		:param inDict:  root菜单树(字典)
		:param tabCount: 缩进的tab数量
		:return: 无
		'''
		if inDict == 'self.menuDict':
			inDict = eval(inDict)

		if isinstance(inDict, list):
			return
		# print("{0}{1}".format('\t'*tabCount, inDict[0]))
		elif isinstance(inDict, dict):
			for key, value in inDict.items():
				if isinstance(value, list):
					print("{0}{1}<{2}>".format('\t' * tabCount, key, value[0]))  # 叶子节点,ECU
				else:
					print("{0}{1}".format('\t' * tabCount, key))  # 系统

				self.ShowAll(value, tabCount + 1)  # 继续递归
		else:  # 参数类型错误
			print(type(inDict))
			raise ValueError
		pass




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


def ReadTextPlus(inFilePath):
	'''
		:param inFilePath: 读inFilePath文件, 如CN_TEXT.txt
		:return: 返回一个字典(按插入顺序排序)
	'''
	if os.path.isfile(inFilePath):
		with open(inFilePath, "r") as lan:
			linesList = lan.readlines()
		# retLanDict = {}
		retDict = OrderedDict()
		for line in linesList:
			if line != "\n":
				fieldCount = len(line.split('\t\t'))
				key = line.split("\t\t")[0]
				valueList = line.split('\t\t')[1:]
				newValueList = []
				for value in valueList:
					if (value[0] == '"') & (value[-1] == '"'):
						newValueList.append(value[1:-1])
					else:
						newValueList.append(value)
				retDict[key] = newValueList
		return retDict



def Add0x(inStr):
	'''
	:param inStr: 例如:   0022334455    
	:return: 返回 0x00,0x22,0x33,0x44,0x55
	'''
	inStr = inStr.strip() #去除空白符
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
	inStr = inStr.strip()
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


def MyHexPlus(inArg):
	'''
	:param inArg: 将一个整数, 或者十进制整数字符串转换为0xAB类型的 
	:return: 
	'''
	tmpStr = hex(int(str(inArg), 10))[2:].upper()
	if (len(tmpStr) & 1):
		tmpStr = '0' + tmpStr
	return Add0x(tmpStr)



def MyHexPlusPlus(inArg, fillLength=1):
	'''
	:param inArg: 将一个整数, 或者十进制整数字符串转换为0xAB类型的 
	:param fillLength :  填充到多少个字节 
	:return: 
	'''
	if(int(str(inArg), 10) <= (2<<(fillLength*8-1))-1):
		tmpLen = len(hex(int(str(inArg), 10))[2:].upper())
		return Add0x('0'*(2*fillLength - tmpLen) + hex(int(str(inArg), 10))[2:].upper())

	tmpStr = hex(int(str(inArg), 10))[2:].upper()
	if (len(tmpStr) & 1):
		tmpStr = '0' + tmpStr
	return Add0x(tmpStr)
