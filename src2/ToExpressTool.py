#!coding:utf8

'''
Date:2017/8/25/9:11
Author:yqq
Description: 将系数转换为表达式,按模式转换
'''
from collections import OrderedDict
from lib.mytool7 import TextTool
from lib.mytool7 import MyHexPlus

def Mode1(DsNo, k1, k2, k4, inLen):
	'''
	:param DsNo: 编号, 用于错误定位
	:param k1: k1  系数1
	:param k2: k2  系数2
	:param k4: k4  系数4 
	:param inLen:   数据长度
	:return: 生成的表达式
	'''

	if "1" == str(inLen):
		if "HEX" in k4:
			retExp = "string y; BYTE x; y=HEX(x);"  #以16进制显示
		elif ("." in k1) | ("." in k2):
			retExp = "float y; BYTE x; y=({0})*x+({1});".format(k1, k2) #浮点型
		else:
			retExp = "int y; BYTE x; y=({0})*x+({1});".format(k1, k2) #整型
			#还有其他类型??
		pass

	elif "2" == str(inLen):
		# 提醒: 如果长度为 2 则按照小端方式转成数值, 然后乘以系数k1, 加上k2
		# 因为底层算法接口, 不支持 "int x;" 这样的声明, 支持 "BYTE x;" 这样的方式
		# 只能将传入的2 个字节分开成 BYTE x1,x2; 这样的方式,然后再将两个 x "合成"为一个;

		#retExp = "int y; BYTE x1,x2; y = (x1 << 8 & 0xFF00) + (x2 & 0xFF)"   #底层算法也不支持左移和右移
		#retExp = "int y; char x1,x2; y=((x1*256)&0xFF00)+(x2&0xFF);" #支持 "char"????


		#此处用小端, 也就是说, 在数据流代码实现时, 就按普通的方式传入参数即可, 无需改变入参x1, x2的顺序
		if ("." in k1) | ("." in k2):
			retExp = "float y; BYTE x1,x2; y=(((x2*256)&0xFF00)+(x1&0xFF))*({0})+({1});".format(k1, k2) #改成乘法的形式
		else:
			retExp = "int y; BYTE x1,x2; y=(((x2*256)&0xFF00)+(x1&0xFF))*({0})+({1});".format(k1, k2) #改成乘法的形式
		pass
	else:
		print("NO{0} : Error in inLen ".format(DsNo))
		raise ValueError

	return retExp



def Mode2(DsNo, k1, k2, k3, k4):
	'''
	:param DsNo: 
	:param k1: 
	:param k2: 
	:param k3: 
	:param k4: 
	:return:    已经解析出来，见分析文档; 在代码里面实现; 部分协议有问题,进不了系统;
	'''

	pass


def Mode3(DsNo, k1, k4):
	'''
	:param DsNo: 编号,用于错误定位 
	:param k4: 控制位,  x & 0x04 != 0  
	:return:  表达式
	'''

	#开启:0x55,0x00,0x99,0x99,0x00,0x04
	#关闭:0x55,0x00,0x99,0x99,0x00,0x03

	if k1 == '1':
		if len(k4) != 0:
			retExp = r'string y; BYTE x; if(x&({0})) y=\"0x55,0x00,0x99,0x99,0x00,0x04\";else y=\"0x55,0x00,0x99,0x99,0x00,0x03\";'.format(
				k4)
			return retExp
		else:
			print("ECUID:{0} error k4 in Mode3()".format(DsNo))
			raise ValueError
	else:
		#读取../txt/Mode3.txt  获取k1对应的算法表达式,并用k4替换表达式中{0}
		#其中,k1=310的两个ecu要特殊处理, 其k4分别为 0xF 和 0xF0

		#此处不需要考虑运行效率(每次都重新打开文件,重新获取,重新查询)
		with open("../txt/Mode3.txt", "r") as inFile:
			lineList = inFile.readlines()
			for line in lineList:
				if len(line) == 0: continue  #空行
				if k1 == line.split('\t\t')[0].strip():
					if(k1 == '310') & (DsNo == '642'): #310的两个ecu特殊处理
						return line.split('\t\t')[2].strip()  #表达式

					if '{0}' in line.split('\t\t')[1].strip(): #如果表达式中有{0} 占位符, 则用k4替之
						return line.split('\t\t')[1].strip().format(k4)
					return line.split('\t\t')[1].strip().format(k4)
			print("{0} -> not found express".format(k1))
			raise ValueError
	pass


def Mode4(DsNo, k2):
	'''
	:param DsNo:  用于错误定位
	:param k2: 入参
	:return:  表达式
	直接在实现代码里面写
	'''

	#retStr = 'string y; BYTE x; y=BTDC ;'.format()

	pass



def Mode33(DsNo,  k2, k3, k4 ):
	'''
	:param DsNo: 用于错误定位  
	:param k2: 
	:param k3: 
	:return:  替换k2后的普通表达式(可以用于数据流算法接口的形式)
	
	'''

	#手动写出表达式, 并在表达式中留占位符,获取k2, 再用k2替换那个占位符即可;

	expDict = {}
	with open("../txt/Mode33.txt", "r") as inFile:
		for line in inFile.readlines():
			expDict[line.split('\t\t')[0].strip()] = line.split('\t\t')[1].strip()

	tmpKey= k3 + ";" +  k4     #组成键值
	if tmpKey in expDict:
		tmpExp = expDict[tmpKey]
	else:
		print("{0}({1})is failed to found.".format(DsNo, tmpKey))
		raise ValueError

	return  tmpExp.format(k2)  #用k2替换原来的占位符




def Mode64(DsNo, k2):
	'''
	:param DsNo: 
	:param k2: 
	:return: 在数据流代码里面实现
	'''
	pass


def Mode65():
	'''
	:return:  此模式未开发
	'''
	pass


def main():

	'''
	1.读out_Ds_Info2.txt,获取系数
	2.调用相应函数生成表达式
	3.将表达式写入文件
	'''

	#1.读out_Ds_Info2.txt,获取系数
	tt = TextTool("../doc/tmp/out_Ds_Info2.txt")

	#tt.ShowAll()

	tmpDict = tt.allSectDictOfFile

	outFile = open("../doc/tmp/out_Express.txt", "w")

	for i in range(303, 1177+1):  #忽略Ecu 为 90001~900010
		tmpSectKey = "0xFF,0xFF,0xFF,0xFF,{0}".format(MyHexPlus(i))
		if tmpSectKey in tmpDict:

			tmpDsNo = tmpDict[tmpSectKey]["Netlayer"]["NO"][0].strip()
			tmpK1 = tmpDict[tmpSectKey]["Netlayer"]["k1"][0].strip()
			tmpK2 = tmpDict[tmpSectKey]["Netlayer"]["k2"][0].strip()
			tmpK3 = tmpDict[tmpSectKey]["Netlayer"]["k3"][0].strip()
			tmpK4 = tmpDict[tmpSectKey]["Netlayer"]["k4"][0].strip()
			tmpLen = tmpDict[tmpSectKey]["Netlayer"]["Length"][0].strip()

			tmpMode = tmpDict[tmpSectKey]["Netlayer"]["DsMode"][0].strip()

			if tmpMode == '1':
				retExp = Mode1(tmpDsNo,tmpK1, tmpK2, tmpK4, tmpLen)
			elif tmpMode == '2':
				continue
			elif tmpMode == '3':
				retExp = Mode3(tmpDsNo, tmpK1, tmpK4)
			elif tmpMode == '4':
				continue
			elif tmpMode == '33':
				retExp = Mode33(tmpDsNo, tmpK2, tmpK3, tmpK4)
			elif tmpMode == '64':
				continue
			elif tmpMode == '65':
				continue
			else:
				raise ValueError

			outFile.write("{0}\t\t\"{1}\"\n".format(tmpSectKey, retExp))

	outFile.close()
	pass


if __name__ == "__main__":

	main()


	from tkMessageBox import showinfo
	showinfo(u'温馨提示', u'请继续执行src6/DealExpress.py\n以完成对doc/tmp/out_Express.txt的处理.(^_^) ')
	pass

	pass