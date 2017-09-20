#!coding:utf8

'''
Date:2017/9/12/8:50
Author:yqq
Description: 用来二次修改Ecu_Info.txt中的一些命令 
'''


from lib.mytool10 import TextTool

def main():

	tt = TextTool("../doc/tmp/out_Ecu_Info.txt")
	# tt.ShowAll()
	# print(len(tt.allSectDictOfFile))

	tmpDict = tt.allSectDictOfFile
	for sectKey, sectDict in tmpDict.items():
		for fieldKey, fieldDict in sectDict.items():
			if "ProtocolName" in fieldDict:
				protName = fieldDict["ProtocolName"][0].strip()


				#普通KWP协议
				if protName == "KWP2000":
					if "KeepLinkCmd" in fieldDict:
						newLinkCmd = fieldDict["KeepLinkCmd"][0].strip()[6 : -2]
						fieldDict["KeepLinkCmd"].pop()
						if (fieldDict["VehEcuId"][0].strip() == "900024"):
							fieldDict["KeepLinkCmd"].append("3E01")
						elif fieldDict["VehEcuId"][0].strip() == "900061":
							fieldDict["KeepLinkCmd"].append("3E")
						else:
							fieldDict["KeepLinkCmd"].append(newLinkCmd)
					if "ComPin" in fieldDict:
						from src3.ComPin import CalcComPin
						newComPin = CalcComPin( fieldDict["ComPin"][0].strip() )
						fieldDict["ComPin"].pop()
						fieldDict["ComPin"].append(newComPin )
					if "ReadDtcCmd" in fieldDict:
						if fieldDict["ReadDtcCmd"][0].strip()[0:2] == "80": #80系列
							newReadDtcCmd = fieldDict["ReadDtcCmd"][0].strip()[8 : -2]
						else: #8X系列
							newReadDtcCmd = fieldDict["ReadDtcCmd"][0].strip()[6 : -2]
						fieldDict["ReadDtcCmd"].pop()
						fieldDict["ReadDtcCmd"].append(newReadDtcCmd)
					if "ClearDtcCmd" in fieldDict:
						newClearDtcCmd = fieldDict["ClearDtcCmd"][0].replace(';', '').strip()[6: -2]
						fieldDict["ClearDtcCmd"].pop()
						fieldDict["ClearDtcCmd"].append(newClearDtcCmd)

				#CAN协议
				if protName == "CAN":
					if "ComPin" in fieldDict:
						from src3.ComPin import CalcComPin
						newComPin = "6,14"
						fieldDict["ComPin"].pop()
						fieldDict["ComPin"].append(newComPin)
					if "ReadDtcCmd" in fieldDict:
						newReadDtcCmd = fieldDict["ReadDtcCmd"][0].strip()[6 : ]
						fieldDict["ReadDtcCmd"].pop()
						fieldDict["ReadDtcCmd"].append(newReadDtcCmd)
					if "ClearDtcCmd" in fieldDict:
						newClearDtcCmd = fieldDict["ClearDtcCmd"][0].replace(';', '').strip()[6 : -2]
						fieldDict["ClearDtcCmd"].pop()
						fieldDict["ClearDtcCmd"].append(newClearDtcCmd)

				#处理KWP地址码进入
				if protName == "KWP_0X":
					if "ComPin" in fieldDict:
						from src3.ComPin import CalcComPin
						newComPin = CalcComPin( fieldDict["ComPin"][0].strip() )
						fieldDict["ComPin"].pop()
						fieldDict["ComPin"].append(newComPin )
					if ("KeepLinkCmd" in fieldDict) & (len(fieldDict["KeepLinkCmd"][0]) != 0):
						newLinkCmd = fieldDict["KeepLinkCmd"][0].strip()[2 : 4]
						fieldDict["KeepLinkCmd"].pop()
						fieldDict["KeepLinkCmd"].append(newLinkCmd)

	#tt.ShowAll()
	tt.WriteFile("../doc/tmp/out_Ecu_Info_new.txt")  #将修改之后的内容重新写到一个新文件

	#tt1 = TextTool("../doc/tmp/out_Ecu_Info_new.txt")
	#tt1.ShowAll()

	pass


if __name__ == "__main__":

	main()

	pass