# 数据流表达式修改1

## 问题

- 由于表达式中的 '&' 和 '==' 运算符优先级问题,导致部分数据流不能显示值



## 解决方案

- 将原来的表达式替换. 例如: 'x&0x7==0' 替换成 '(x&0x7)==0'

- 使用正则表达式 'x&0x[0-Z]{1,2}==' 匹配 ; 然后添加上 '()' 即可


# 数据流表达式修改2

## 问题
- 例如"y=(1.1925)*x+(-152.399994)" 不能被正确计算,需改成y=(1.1925)*x-152.399994"

## 解决方法

- 用正则表达式, r'\+\(.*?\)'  匹配 加一个负数的子串
- 去掉括号即可



