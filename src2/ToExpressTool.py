#!coding:utf8

'''
Date:2017/8/25/9:11
Author:yqq
Description: 将系数转换为表达式,按模式转换
'''

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
			retExp = "float y; BYTE x; y={0}*x+{1};".format(k1, k2) #浮点型
		else:
			retExp = "int y; BYTE x; y={0}*x+{1};".format(k1, k2) #整型
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
			retExp = "float y; BYTE x1,x2; y=((x2*256)&0xFF00)+(x1&0xFF);" #改成乘法的形式
		else:
			retExp = "int y; BYTE x1,x2; y=((x2*256)&0xFF00)+(x1&0xFF);" #改成乘法的形式
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
	:return:     协议有问题,进不了系统
	'''

	pass


def Mode3(DsNo, k4):
	'''
	:param DsNo: 编号,用于错误定位 
	:param k4: 控制位,  x & 0x04 != 0  
	:return:  表达式
	'''

	#开启:0x55,0x00,0x99,0x99,0x00,0x04
	#关闭:0x55,0x00,0x99,0x99,0x00,0x03

	if len(k4) != 0:
		retExp = 'string y; BYTE x; if(x&{0}) y=\"0x55,0x00,0x99,0x99,0x00,0x04\";\
				else y=\"0x55,0x00,0x99,0x99,0x00,0x03\";'.format(k4)
		return retExp
	else:
		print("ECUID:{0} error k4 in Mode3()".format(DsNo))
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



def Mode33(DsNo,  k2, k3, k4, inExp ):
	'''
	:param DsNo: 用于错误定位  
	:param k2: 
	:param k3: 
	:param k4: 
	:param inExp: 
	:return:  替换k2后的普通表达式(可以用于数据流算法接口的形式)
	'''

	retExp = ""



	#手动写出表达式, 并在表达式中留标识符,获取k2, 再替换那个标识符,即可;


	return retExp




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

	pass


if __name__ == "__main__":

	main()

	pass