#!coding:utf8

'''
Date:2017/8/22/16:11
Author:yqq
Description:none
'''

from lib.mytool6 import ReadText


def main():

	n1 = ReadText("../txt/cmp/new1.txt")
	n2 = ReadText("../txt/cmp/new2.txt")

	s1 = set()
	for key, value in n1.items():
		s1.add(value)

	s2 = set()
	for key, value in n2.items():
		s2.add(value)

	s3 = s1 - s2   #求差集

	for item in s3:
		print(item)

	pass


if __name__ == "__main__":

	main()

	pass