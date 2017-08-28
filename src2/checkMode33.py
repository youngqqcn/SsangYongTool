#!coding:utf8

'''
Date:2017/8/28/14:47
Author:yqq
Description:检查模式33算法
'''

def IsOk(inStr):
	'''
	:param inStr: 算法表达式
	:return: 合法: 1 ; 不合法: 0
	'''

	if (inStr.count(r'\"') & 1) != 0: #检查\"
		print("\\\"is not match")
		return False
	if (inStr.count(r'(') != inStr.count(r')')):  #检查括号
		print("() in not match")
		return False

	return True

	pass


def main():

	with open("../txt/Mode33.txt", "r") as inFile:
		lineList = inFile.readlines()
		for line in lineList:
			if not IsOk(line.split('\t\t')[1]):
				print line.split('\t\t')[0]
	pass


if __name__ == "__main__":

	main()

	pass