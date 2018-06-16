#!/usr/bin/python
#coding:utf-8

# 全排列字典生成器

f = open("dict.txt", "w+")
chars = ["demon","admin","888"]   #指定密码关键字
base = len(chars)

for i in range(0, base):
	for j in range(0, base):	
		for k in range(0, base):
			for l in range(0, base):
				for m in range(0, base):
					for n in range(0, base):
						ch0 = chars[i];
						ch1 = chars[l];
						ch2 = chars[k];
						ch3 = chars[l];
						ch4 = chars[m];
						ch5 = chars[n];
						print ch0,ch1,ch2,ch3,ch4,ch5
						f.write(ch0+ch1+ch2+ch3+ch4+ch5+"\n\r")
f.close()
print "Ok!!"
