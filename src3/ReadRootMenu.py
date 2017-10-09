#!coding:utf8

'''
Date:2017/8/29/11:51
Author:yqq
Description:读root菜单
'''

import  os
from collections import OrderedDict
from lib.mytool8 import RootMenu



def IsLeafNode(inStr):
	'''
	:param inStr: 节点字符串
	:return: 如果是叶子节点返回True; 否则返回False
	'''
	inStr = inStr.strip()
	if ('<' in inStr) & ('>' in inStr):
		return True
	return False


def GetLeafNodeNameAndID(inStr):
	'''
	:param inStr: 节点字符串, 比如:   安全气囊<900021> 
	:return: 返回节点名称(Ecu名称)和节点ID(ECU ID)
	'''

	inStr = inStr.strip()
	if ('<' in inStr) & ('>' in inStr):
		return [inStr[ : inStr.find('<')], inStr[inStr.find('<')+1 : inStr.find('>')]]
	raise ValueError


def GetSubNode(inList):
	'''
	:param inList: 剩余节点链表(还未处理的节点列表)
	:return: inList[0] 下所有子节点组成的列表, 所有这些处理过的子节点都会从inList中永久删除
	'''

	# 获取此节点下所有子节点,同时删掉以处理掉的节点
	parentNode = inList[0]     #将第一个作为父节点
	inList.remove(inList[0])   #永久删除已经处理的parentNode这个节点,注意remove()是没有返回值
	if len(inList) == 0:
		return []

	tmpNodeList = []
	while True:
		if len(inList) == 0: #节点列表空了
			break
		if inList[0].count('\t') > parentNode.count('\t'):  #即字节点的tab的数量一定大于父节点
			tmpNodeList.append(inList[0])
			inList.remove(inList[0]) #删掉已经处理过的节点
		else:
			break
	return tmpNodeList



def AddMenuItem(inDict, nodeList):
	'''
	:param inDict: 传入传出参数, 菜单树(字典)
	:param nodeList: 剩余的节点列表
	:return: 无
	'''

	#算法设计(递归)
	#1.如果是叶子节点,将此节点挂在其父节点下面; --->递归边界条件
	#2.如果不是叶子节点,将此节点的所有子节点挂上来, 再把此节点挂在其父节点上;
	#3.再处理其他节点

	if (nodeList == None) | (nodeList == []) :
		return
	if IsLeafNode(nodeList[0]): #1.如果是叶子节点, 将此节点挂在其父节点下面; --->递归边界条件
		inDict[GetLeafNodeNameAndID(nodeList[0])[0]] = [GetLeafNodeNameAndID(nodeList[0])[1]]
		nodeList.remove(nodeList[0])
		AddMenuItem(inDict, nodeList)
	else:
		tmpDict = OrderedDict()
		tmpNode = nodeList[0]
		subNodeList = GetSubNode(nodeList)

		AddMenuItem(tmpDict,  subNodeList) #2.将此节点下的所有子节点挂上来
		inDict[tmpNode.strip()] = tmpDict  #再把此节点挂在其父节点上

		AddMenuItem(inDict, nodeList)  #3.再处理其他的节点

	pass




def ShowAll(inDict, tabCount = 0):
	'''
	:param inDict:  root菜单树(字典)
	:param tabCount: 缩进的tab数量
	:return: 无
	'''

	if isinstance(inDict, list):
		return
		#print("{0}{1}".format('\t'*tabCount, inDict[0]))
	elif isinstance(inDict, dict):
		for key, value in inDict.items():
			if isinstance(value, list):
				print("{0}{1}<{2}>".format('\t'*tabCount, key, value[0])) #叶子节点,ECU
			else:
				print("{0}{1}".format('\t'*tabCount, key)) #系统

			ShowAll(value, tabCount + 1)  #继续递归
	else: #参数类型错误
		print(type(inDict))
		raise ValueError
	pass


def ReadRootMenu(inFilePath):

	if  os.path.isfile(inFilePath):
		with open(inFilePath, "r") as inFile:
			lineList = inFile.readlines()
			lineList.remove(lineList[0])
			retDict = OrderedDict()
			AddMenuItem(retDict, lineList)
			#print(len(retDict))
			ShowAll(retDict, 0)
			#print(retDict)
			pass
	pass


def main():

	#retDict = ReadRootMenu("../txt/TestRootMenu.txt")
	rm = RootMenu("../txt/TestRootMenu.txt")
	rm.ShowAll()

	pass


if __name__ == "__main__":

	main()

	pass