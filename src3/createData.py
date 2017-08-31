#!coding:utf8

'''
Date:2017/8/29/11:17
Author:yqq
Description:生成模拟平台的数据
'''

from lib.mytool7 import *
from src3.ComPin import CalcComPin    #计算引脚的算法


gKwpHeaderStr = '''\
[SETTING]
	PROT=KWP
	BPS={0}
	PIN={1},{1}
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





def GetHistoryCmdData(inEcuId ):
	'''
	:param inEcuId: ecuID     
	:return: 
	#如果需要重新生成平台数据, 又要保留原来的"命令数据"(不含底层配置信息),
	#只要将txt/byEcu目录下的文件替换掉为原来的文件即可
	'''

	retList = []
	with open("../txt/byEcu/{0}.txt".format(inEcuId), "r") as inFile:
		lineList = inFile.readlines()
		flag = False
		for line in lineList:
			if flag :
				retList.append(line)
			if '[COMMAND]' in line:
				flag = True
	if len(retList) == 0:
		retList.append('\n\n')
	return retList



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

			# 其中900041的引脚为空,经过检测,是13引脚,且已验证(在Ecu_Info.txt中手动添加了)
			comPin =  tmpDict[sectKey][fieldKey]["ComPin"][0].strip()

			if comPin == '':
				print(ecuId)
			if "KWP" in protName.upper(): #KWP????
				header = gKwpHeaderStr.format(bauteRate, CalcComPin(comPin))  #ComPin函数计算引脚
			elif "CAN" in protName.upper():
				header = gCanHeaderStr.format(bauteRate)
			else: #其他协议
				continue

			#重新生成的平台数据在"../doc/out_CarData/"目录下
			with open("../doc/out_CarData/{0}.txt".format(ecuId), "w") as outFile:
				outFile.write(header + "\n")

				#写入原来的平台数据(除底层配置信息以外)
				# 如果不想保留原来平台数据,注释此句即可
				outFile.writelines(GetHistoryCmdData(ecuId))

	pass


if __name__ == "__main__":

	main()

	pass