#!coding:utf8

'''
Date:2017/8/31/18:42
Author:yqq
Description: 解通信引脚
'''

# coding:utf8

from Tkinter import *


def ComPin(inVar):
	'''
	:param inVar: 输入引脚, 如 0x0800 表示引脚14
	:return: 解出来的引脚 14
	'''

	# 4, 5, 16 号引脚是电源, 不能用
	tmpDict = {
		0x0001: 1, 0x0002: 2, 0x0004: 3, 0x0008: 6,
		0x0010: 7, 0x0020: 8, 0x0040: 9, 0x0080: 10,
		0x0100: 11, 0x0200: 12, 0x0400: 13, 0x0800: 14,
		0x1000: 15
	}

	if '0x' in inVar:
		tmpStr = inVar[2:] #去掉'0x'
	else:
		tmpStr = inVar
	if tmpStr == '':
		print('helleo')

	if int(tmpStr, 16) in tmpDict:
		return str(tmpDict[int(tmpStr, 16)])
	else:
		return 'Error'
	pass

def GetComPin(event):

	outVar1.set(ComPin(inVar1.get()))

	pass




if __name__ == '__main__':

	master = Tk()

	rF1 = Frame(master, borderwidth=5)
	f1 = Frame(rF1, pady=5)
	Label(f1, text="输入:").pack(side=LEFT)
	inVar1 = StringVar()
	e1 = Entry(f1, textvariable=inVar1)
	e1.bind('<Key-Return>', GetComPin)
	e1.pack(side=RIGHT)
	f1.pack(side=TOP)

	f2 = Frame(rF1, pady=5)
	Label(f2, text="引脚:").pack(side=LEFT)
	outVar1 = StringVar()
	Entry(f2, textvariable=outVar1).pack(side=RIGHT)
	f2.pack(side=TOP)

	f3 = Frame(rF1, pady=5)
	Button(f3, text="确定", command=GetComPin, width=10).pack(side=RIGHT)
	f3.pack(side=TOP)

	rF1.pack(side=LEFT)

	master.title("双龙引脚")
	# master.iconbitmap()
	master.resizable(width=False, height=False)
	master.mainloop()
	pass


