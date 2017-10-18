#!coding:utf8

'''
Date:2017/10/18/9:17
Author:yqq
Description: 
	尝试对菜单索引进行加密处理,但是,因为代码里面有很多地方直接用了索引...
	只好不加密,暂时不加密
	
	在V30.00以后的版本可以参考源码进行加密
'''

import os
import hashlib


def GetStrCRC32(instr):
	'''
	获取字符串的CRC32校验码
	:param instr: 
	:return: 
	'''

	m_pdwCrc32Table = [0 for x in range(0, 256)]
	dwPolynomial = 0xEDB88320
	for i in range(0, 255):
		dwCrc = i
		for j in [8, 7, 6, 5, 4, 3, 2, 1]:
			if dwCrc & 1:
				dwCrc = (dwCrc >> 1) ^ dwPolynomial
			else:
				dwCrc >>= 1
		m_pdwCrc32Table[i] = dwCrc
	dwCrc32 = 0xFFFFFFFFL
	for i in instr:
		b = ord(i)
		dwCrc32 = ((dwCrc32) >> 8) ^ m_pdwCrc32Table[(b) ^ ((dwCrc32) & 0x000000FF)]
	dwCrc32 = dwCrc32 ^ 0xFFFFFFFFL
	return dwCrc32


def GetFileCRC32(filepathname):
	'''
	获取文件的CRC32校验码
	:param filepathname: 
	:return: 
	'''
	import binascii
	try:
		uf = open(unicode(filepathname,'utf8'),"rb")
		ucrc = binascii.crc32(uf.read())
		uf.close()
		if ucrc>0:
			uoutint=ucrc
		else :
			uoutint= ~ucrc^0xffffffff
		return '%x' % (uoutint)
	except:
		return ''


def GetMD5(filePath):
	'''
	获取一个文件的md5
	:param filePath: 
	:return: 
	'''

	if  os.path.isfile(filePath):
		with open(filePath, "rb") as inFile:
			md5Obj = hashlib.md5()
			md5Obj.update(inFile.read())
			md5Code = str(md5Obj.hexdigest()).lower()
		return md5Code
	return ""


def main():

	#print(GetMD5("../doc/out_SsangYong/900011.txt"))
	with open("../doc/out_SsangYong/900011.txt", "r") as inFile:
		print (GetStrCRC32(inFile.read()))


	pass


if __name__ == "__main__":

	main()

	pass