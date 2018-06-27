#coding: utf-8
#author: demon
#date: 2018-04-24

filename = input("Enter the filename: ")
keyword = input("Enter the keywords: ")
content = open(filename,"r").read()
print len(content.split(keyword)) - 1


