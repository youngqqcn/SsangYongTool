#!coding:utf8

'''
Date:2017/9/6/14:37
Author:yqq
Description:检查数据流模式3的算法表达式是否合法(如: 括号是否匹配等)
'''

def IsOk(inStr):
	'''
	:param inStr: 算法表达式
	:return: 合法: 1 ; 不合法: 0
	'''

	if (inStr.count(r'\"') & 1) != 0: #检查\"
		print("\\\"is not match")
		return False
	if (inStr.count(r'(') != inStr.count(r')')):  #检查括号是否匹配
		print("() in not match")
		return False

	return True

	pass


def main():

	with open("../txt/Mode3.txt", "r") as inFile:
		lineList = inFile.readlines()
		for line in lineList:
			if len(line) == 0: continue

			tmpK1 = line.split('\t\t')[0]
			tmpExp = line.split('\t\t')[1:]  #算法表达式
			if not IsOk(tmpExp) :
				print ("{0}".format(tmpK1))
				break

	pass


if __name__ == "__main__":

	main()

	pass