#!coding:utf8

'''
Date:2017/9/27/14:50
Author:yqq
Description:none
'''

import  re
import os


def main():

	pattern = re.compile(r'x&0x[0-Z]{1,2}==')
	pattern2 = re.compile(r'\+\(\-.*?\)')

	if os.path.exists("../doc/tmp/new_out_Express.txt"):
		os.remove("../doc/tmp/new_out_Express.txt")

	with open("../doc/tmp/out_Express.txt", "r") as inFile:
		lineList = inFile.readlines()
		with open("../doc/tmp/new_out_Express.txt", "w") as outFile:
			for eachLine in lineList:
				findList = pattern.findall(eachLine)
				if (len(findList) > 0):
					for eachFind in findList:
						newStr = '(' + eachFind[:-2] + ')=='
						if eachFind in eachLine:
							eachLine = eachLine.replace(eachFind, newStr)
					pass

				findList2 = pattern2.findall(eachLine)
				if(len(findList2) > 0):
					for eachFind in findList2:
						newStr = eachFind[2:-1]
						if eachFind in eachLine:
							eachLine = eachLine.replace(eachFind, newStr)

				outFile.write(eachLine)

	pass


if __name__ == "__main__":

	main()

	pass