#!coding:utf8

'''
Date:2017/9/26/17:47
Author:yqq
Description:none
'''

import os
import sys
import shutil
import  tempfile

def main():

	if os.path.exists("../txt/Ecu_Info.txt"):
		print("hello")
		shutil.copy("../txt/Ecu_Info.txt", "hello.txt")

	pass


if __name__ == "__main__":

	main()

	pass