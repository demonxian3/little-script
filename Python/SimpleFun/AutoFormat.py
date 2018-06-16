#coding: utf-8
#author: demon
#date: 2018-04-24

from __future__ import print_function
import re

inputFile = input("Enter input filename: ")
outputFile = input("Enter output filename: ")


fpr = open(inputFile, "r")
fpw = open(outputFile, "w")


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

TabLen = 0

#1 15 15 22 25

beginElems = ["<body", "<table", "<tbody", "<tr", "<td","<p","<div","<a","<span"]
endElems   = ["</body", "</table", "</tbody", "</tr", "</td","</p","</div","</a","</span"]



isCSS = False

for i in preArr:

	# CSS Format
	if "<style" in i:
		isCSS = True
		fpw.write("    "*TabLen + i + "\r\n")
		continue

	if "</style" in i:
		isCSS = False
		fpw.write("    "*TabLen + i + "\r\n")
		continue

	if isCSS:
		i = re.sub("[ ]", "", i);
		for j in i:

			if j == ';':
				fpw.write(j + "\r\n")

			elif j == '{' or j == '}':
				fpw.write("    "*TabLen + j + "\r\n")

			else:
				fpw.write(j)
	

	#HTML Format
	isBreak = False
	for j in beginElems:
		if j in i:
			TabLen += 1
			fpw.write("    "*TabLen + i + "\r\n")
			isBreak = True
			break

	if not isBreak:
		for j in endElems:
			if j in i:
				fpw.write("    "*TabLen + i + "\r\n")
				TabLen -= 1
				isBreak = True
				break

	
	if not isBreak:
		fpw.write("    "*TabLen + i + "\r\n")
		




fpw.close()
fpr.close()








