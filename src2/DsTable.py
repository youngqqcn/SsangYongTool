#!coding:utf8

'''
Date:2017/8/30/9:23
Author:yqq
Description:none
'''

from lib.mytool8 import TextTool
from lib.mytool8 import ReadText
from lib.mytool8 import MyHexPlus


def GetDsName(inDsNameNo, cnDsDict):
	'''
	:param inDsNameNo: 数据流名称
	:param cnDsDict: 文本库
	:return: 如果找到则返回数据流名称文本; 否则引发异常
	'''

	if int(str(inDsNameNo).strip(), 10) <= 255:
		index = "0x55,0x43,0x67,0x10,0x00," + MyHexPlus(inDsNameNo)
	else:
		index = "0x55,0x43,0x67,0x10," + MyHexPlus(inDsNameNo)

	if index in cnDsDict:
		return cnDsDict[index]
	else:
		print("inDsNameNo:{0}".format(inDsNameNo))
		print("index:{0}".format(index))
		print("not found DsName in cnDsDict")
		raise ValueError
	pass



def GetDsUnit(inDsUnitNo, cnDsDict):
	'''
	:param inDsUnitNo: 数据流单位
	:param cnDsDict: 文本库
	:return: 如果找到返回数据流单位文本, 否则引发异常
	'''
	if int(str(inDsUnitNo).strip(), 10) <= 255:
		index = "0x55,0x43,0x67,0x20,0x00," + MyHexPlus(inDsUnitNo)
	else:
		index = "0x55,0x43,0x67,0x20," + MyHexPlus(inDsUnitNo)

	if index in cnDsDict:
		if cnDsDict[index].strip() == "":
			return " "
		return cnDsDict[index]
	else:
		print("not found DsUnit in cnDsDict")
		raise ValueError
	pass


def WriteDsTable(outFile, *argList):
	'''
	:param outFile: 输出文件
	:param argList: 可变参数列表; 包含了ecuId, dsName, dsCmd,  ....等数据
	:return: 无
	'''

	#如果文本库是GB2312编码,打开以下注释即可,输出文件是utf-8
	for arg in argList[:-1]: #除了最后一个
		if len(arg) == 0: #为空
			arg = "  "  #设置为空格填充,保证excel表格的整体格式
		outFile.write("{0}\t".format(arg.decode('gb2312').encode('utf8')))
	outFile.write("{0}\n".format(argList[-1:][0]).decode('gb2312').encode('utf-8')) #最后一个后面是换行符

	#如果文本库是utf-8编码,打开以下注释即可, 输出文件也是utf-8
	# for arg in argList[:-1]: #除了最后一个
	# 	outFile.write("{0}\t".format(arg))
	# outFile.write("{0}\n".format(argList[-1:][0])) #最后一个后面是换行符

	pass


def main():

	tt = TextTool("../doc/tmp/out_DS_Info2.txt")
	expDict = ReadText("../doc/tmp/out_Express.txt")
	cnDsDict = ReadText("../txt/cn_ds.txt")

	outFile = open("../doc/tmp/out_Ds_Table.txt", "w")
	#outFile.write("ECUID\t数据流名称\t数据流命令\t控制字节\t长度\t算法表达式\t单位\n")

	tmpDict = tt.allSectDictOfFile
	for sectKey in tmpDict:
		for fieldKey in tmpDict[sectKey]:

			tmpDsMode = tmpDict[sectKey][fieldKey]["DsMode"][0].strip()

			ecuId = tmpDict[sectKey][fieldKey]["EcuID"][0].strip()
			dsName = GetDsName( tmpDict[sectKey][fieldKey]["DsName"][0].strip() , cnDsDict)
			dsCmd = tmpDict[sectKey][fieldKey]["DsCmd"][0].strip()
			ctrlByte = tmpDict[sectKey][fieldKey]["CtrlByte"][0].strip()
			length = tmpDict[sectKey][fieldKey]["Length"][0].strip()
			dsMode = tmpDict[sectKey][fieldKey]["DsMode"][0].strip()
			k1 = tmpDict[sectKey][fieldKey]["k1"][0].strip()
			k2 = tmpDict[sectKey][fieldKey]["k2"][0].strip()
			k3 = tmpDict[sectKey][fieldKey]["k3"][0].strip()
			k4 = tmpDict[sectKey][fieldKey]["k4"][0].strip()

			if int(tmpDsMode, 10) in [2, 4, 64, 65]: #2,4,64模式直接在代码里面实现,不搞算法表达式, 65模式未开发
				if int(tmpDsMode, 10) == 65: #65模式未开发
					continue
				dsExpress = u"在实现代码里面实现".encode('gb2312')
			else:
				dsExpress = expDict[sectKey] #数据流算法索引就是sectKey
			dsUnit = GetDsUnit( tmpDict[sectKey][fieldKey]["DsUnit"][0].strip(), cnDsDict)

			WriteDsTable(outFile, ecuId, dsName, dsCmd, ctrlByte, length,\
			             dsMode, k1, k2, k3, k4, dsExpress, dsUnit)
			pass
	outFile.close()
	pass


if __name__ == "__main__":

	main()

	pass