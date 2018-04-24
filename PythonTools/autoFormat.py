#coding: utf-8
#author: demon
#date: 2018-04-24

from __future__ import print_function
import re


fpr = open("target.txt", "r")
fpw = open("final.txt","w")


# pre process
preHTML = ""
res = fpr.read().split(">")

for i in res:
	i = re.sub("[\r\n\t]", "", i)
	res_length = len(i)

	p = ""
	for j in range(res_length):
		p += i[j]
		if j < res_length-3 and i[j+1] is "<" and i[j+2] is "/":
			p += "\r\n"
	
	if i != "":
		#fpw.write(p+">\r\n")
		preHTML += p + ">\r\n" 



# HTML Tab
preArr = preHTML.split("\r\n")

myStack = []
myLen = 0

#1 15 15 22 25
["body", "table", "tbody", "tr", "td"]



isCSS = False

for i in preArr:

	# CSS Format
	if "<style" in i:
		isCSS = True
		fpw.write("    "*myLen + i + "\r\n")
		continue

	if "</style" in i:
		isCSS = False
		fpw.write("    "*myLen + i + "\r\n")
		continue

	if isCSS:
		i = re.sub("[ ]", "", i);
		for j in i:

			if j == ';':
				fpw.write(j + "\r\n")

			elif j == '{' or j == '}':
				fpw.write("    "*myLen + j + "\r\n")

			else:
				fpw.write(j)
	

	#HTML Format
	if "<td" in i:
		myStack.append(0)
		myLen += 1
		fpw.write("    "*myLen + i + "\r\n")
		continue


	if "</td" in i:
		fpw.write("    "*myLen + i + "\r\n")
		myStack.pop()
		myLen -= 1
		continue

	if "<tr" in i:
		myStack.append(0)
		myLen += 1
		fpw.write("    "*myLen + i + "\r\n")
		continue


	if "</tr" in i:
		fpw.write("    "*myLen + i + "\r\n")
		myStack.pop()
		myLen -= 1
		continue

	if "<tbody" in i:
		myStack.append(0)
		myLen += 1
		fpw.write("    "*myLen + i + "\r\n")
		continue


	if "</tbody" in i:
		fpw.write("    "*myLen + i + "\r\n")
		myStack.pop()
		myLen -= 1
		continue

	if "<body" in i:
		myStack.append(0)
		myLen += 1
		fpw.write("    "*myLen + i + "\r\n")
		continue


	if "</body" in i:
		fpw.write("    "*myLen + i + "\r\n")
		myStack.pop()
		myLen -= 1
		continue

	else:
		fpw.write("    "*myLen + i + "\r\n")




fpw.close()
fpr.close()








