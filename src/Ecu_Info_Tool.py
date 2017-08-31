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


gFiledKeyList = [
	"No",
	"??????", #空的
	"EcuId",
	"ProtocolName",
	"EnterCmd",
	"EnterReply",
	"??Mask1??",
	"BauteRate",
	"AddrCode",
	"KeepLinkCmd",
	"ComPin",
	"ReadDtcCmd",
	"DtcReply",
	"DtcBegin",
	"DtcLen",
	"DtcShowMode",
	"??Mode??",
	"ClearDtcCmd",
	"ClearReply",
	"?????" #空的
]

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
					indexStr = MyHex(int(splitedList[2], 10) - 900000)
					outFile.write("0xFF,0xFF,0xFF,0xFF,0xFF,{0}\t\t\"\\\n".format(indexStr))
					outFile.write("[Netlayer]\t\t\t\t\t\\n\\\n")

					#print(len(splitedList))
					for i in range(0, len(splitedList)):
						if (1 == i) | (0 == i): continue
						#print("{0}={1}".format("\t????" ,  splitedList[i]))
						print("{0}={1}".format("\t" + gFiledKeyList[i], splitedList[i]))

						outFile.write("{0}={1}\t\t\t\t\t\\n".format(
							"\t" + gFiledKeyList[i], splitedList[i]))
						if i + 2 == len(splitedList):
							outFile.write("\"\n\n")
							break
						else:
							outFile.write("\\\n")

		outFile.close()
	else:
		print("error in ReadTabTextFile(): filePath is not a file.")
	pass




def main():

	ReadTabTextFile("../txt/Ecu_Info.txt")

	pass

if __name__ == "__main__":

	main()

	pass