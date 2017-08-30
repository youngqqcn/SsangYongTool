#!coding:utf8

'''
Date:2017/8/29/11:17
Author:yqq
Description:生成模拟平台的数据
'''

from lib.mytool7 import *



gKwpHeaderStr = '''\
[SETTING]
	PROT=KWP
	BPS={0}
	PIN=7,15
	THREAD=
	PARAM=		;空时表示K线进入；脉冲进系统：PARAM=25,25；地址码进系统：PARAM=01,55,D0,8F,~KW2,~ADDR
	CS=ADD
	P1=5
	P2=50
	P3=3
	P4=0
[COMMAND]

'''

gCanHeaderStr = '''\
[SETTING]
	PROT=CAN
	BPS=500k
	PIN=6,14
	THREAD=
	PARAM=
	CS=
	P1=50
	P2=500
	P3=25
	P4=5
	P5=500
[COMMAND]

'''



def main():

	tt = TextTool("../doc/tmp/out_Ecu_Info.txt")
	# tmpHeader = gHeaderStr.format("KWP", "10416", "7,15")
	# with open("test.txt", "w") as outFile:
	# 	outFile.write(tmpHeader)


	tmpDict = tt.allSectDictOfFile
	for sectKey in tmpDict:
		for fieldKey in tmpDict[sectKey]:
			ecuId = tmpDict[sectKey][fieldKey]["EcuId"][0].strip()
			if int(ecuId, 10) <= 900010:continue
			protName = tmpDict[sectKey][fieldKey]["ProtocolName"][0].strip()
			bauteRate = tmpDict[sectKey][fieldKey]["BauteRate"][0].strip()
			if "KWP" in protName.upper(): #KWP????
				header = gKwpHeaderStr.format(bauteRate)
			elif "CAN" in protName.upper():
				header = gCanHeaderStr.format(bauteRate)
			else: #其他协议
				continue
			with open("../doc/out_CarData/{0}.txt".format(ecuId), "w") as outFile:
				outFile.write(header + "\n")

	pass


if __name__ == "__main__":

	main()

	pass