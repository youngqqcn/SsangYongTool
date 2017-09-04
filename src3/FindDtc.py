#!coding:utf8

'''
Date:2017/9/4/11:33
Author:yqq
Description: 
一,故障码的查找有两种方式: 
	第1种: 0x55,0x05,0x06,0x00,  + 码号(即回复内容)
	第2种: 0x55,0x43,0x67,0xA0,  + 故障码序号的16进制

二,遇到问题:
	不确定到底该按照哪种方式进行查找

三,解决方案
	1.列出交集
	2.验证交集

'''

from lib.mytool8 import TabTextTool
from lib.mytool8 import Add0x
from lib.mytool9 import ReadTextPlus
from lib.mytool9 import MyHexPlusPlus

gDtcKeyList = [
	'no',
	'NO-USE',
	'EcuID',
	'DtcCode',
	'DtcNo'
]

gDtcTextKeyList = [
	'index',
	'NO-USE',
	'pcbuCode',
	'NO-USE',
	'dtcText'
]



def main():

	tt = TabTextTool("../txt/Ecu_Dtc.txt", gDtcKeyList)
	#tt.ShowAll()


	print("=================")

	retDict2 = ReadTextPlus("../txt/cn_dtc.txt")


	Count = 0
	countList = []
	countDict1 = {}
	countDict2 = {}
	ecuIDDict = {}

	firstSet = set()  #第 1 种查找方式的 ecuId 集合
	secondSet = set() #第 2 种查找方式的 ecuId 集合

	for eachLineDict in tt.allNamedSplitedList:

		tmpEcuID = int(eachLineDict["EcuID"], 10)

		#if tmpEcuID != 900011: continue

		if tmpEcuID not in ecuIDDict:
			ecuIDDict[tmpEcuID] = 1
		else:
			ecuIDDict[tmpEcuID] += 1
		if int(eachLineDict["EcuID"], 10) <= 900010:
			continue
		tmpDtcCode = eachLineDict["DtcCode"]
		tmpDtcNo = eachLineDict["DtcNo"]
		if ('0x55,0x05,0x06,0x00,' + Add0x(tmpDtcCode)) in retDict2:
			print("{0}>1:{1}-->0x55,0x05,0x06,0x00,{2}".format(tmpEcuID, tmpDtcNo, Add0x(tmpDtcCode)))
			firstSet.add(tmpEcuID)
			if tmpEcuID not in countDict1:
				countDict1[tmpEcuID] = 1
			else:
				countDict1[tmpEcuID] += 1
		#if (tmpEcuID == 900011):
			#print(">" + str(tmpDtcNo))
		if ('0x55,0x43,0x67,0xA0,' + MyHexPlusPlus(tmpDtcNo, 2)) in retDict2:
			print("{0}>2:{1}".format(tmpEcuID, tmpDtcNo))
			secondSet.add(tmpEcuID)
			if tmpEcuID not in countDict2:
				countDict2[tmpEcuID] = 1
			else:
				countDict2[tmpEcuID] += 1
		else:
			print("error:两个种方式都找不到" + str(tmpDtcNo))

		if False:
			if ('0x55,0x05,0x06,0x00,' + Add0x(tmpDtcCode) in retDict2):
				if ('0x55,0x43,0x67,0xA0,' + MyHexPlusPlus(tmpDtcNo, 2) in retDict2):
					Count += 1
					if tmpEcuID not in countList:
						countList.append(tmpEcuID)
					print("{0}->{1}".format(tmpEcuID, tmpDtcNo))
					# print('0x55,0x05,0x06,0x00,' + Add0x(tmpDtcCode) )
					# print('0x55,0x43,0x67,0xA0,' + MyHexPlusPlus(tmpDtcNo, 2))
					print("----------")

	#print("Count is :" + str(Count))
	#print("CountEcuID is : {0}".format(len(countList)))
	#print(countList)
	print('--------')

	print("交集:{0}".format( firstSet & secondSet) )
	print("交集的长度:{0}".format( len(firstSet & secondSet) ))
	for eachEcuId in (firstSet & secondSet):
		#if eachEcuId != 900051: continue
		print("{0}共计:{1}".format( eachEcuId, ecuIDDict[eachEcuId]) )
		print("dict1:{0}".format( countDict1[eachEcuId]) )

		print("dict2:{0}".format( countDict2[eachEcuId]) )
		print('-------')


	print("只有第一种的个数:{0}".format(len(firstSet - secondSet)) )
	print("只有第一种的:")
	for eachEcuId in (firstSet - secondSet): #只有第一种
		print(eachEcuId)

	print("只有第二种的个数:{0}".format(len(secondSet - firstSet)))
	print("只有第二种的:")
	for eachEcuId in (secondSet - firstSet): #只有第一种
		print(eachEcuId)
	pass


if __name__ == "__main__":

	main()

	pass