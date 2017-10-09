#!coding:utf8

'''
Date:2017/8/14/11:04
Author:yqq
Description: 处理tab键分隔的文件
'''
import os

class TabTextTool:

	'''
	处理制表符分隔的文件类
	数据结构: 一行一个列表
	'''

	def __init__(self, inFilePath):
		self.inFilePath = inFilePath
		self.allSplitedLineList =  self.ReadTabFile(inFilePath)

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

	def ShowAll(self ):
		inList = self.allSplitedLineList
		for eachLine in inList:
			print("\n==============")
			for eachFiled in eachLine:
				print("{0}={1}\n".format("????", eachFiled))

