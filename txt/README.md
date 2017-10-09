## 说明(不需改代码)

System_Info_New.txt 和 System_Info.txt 可能因为文件格式的问题, 会多出一个空行

在使用TabText这个类时, 莫名其妙会多出"一列", 我之前没有改变文件格式, 而是顺应
原来的**文件格式**, 多加了一列(即一个字段), 但是后来在 Info_Dtc_Ds_Tool.py中我改变了原来的System_Info.txt文件格式
去掉了那些莫名其妙地空行, 使用TabText类时, 设定的字段数就是实际的列数.


 综上所述, 除了Info_Dtc_Ds_Tool.py这个文件使用System_Info_New.txt(新的), 其他的都使用System_Info.txt(老的)


代码中我已经区分了System_Info_New.txt 和 System_Info.txt, 所有的代码都可以正确运行






