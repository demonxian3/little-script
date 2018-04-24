#coding: utf-8
#author: demon
#date: 2018-04-24

import sys
import os
import urllib  
import urllib2  
import httplib

# https://www.qiushibaike.com/text/
def getRealAddr_urllib2():
    try:
        url="https://www.qiushibaike.com/text/"
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        req = urllib2.Request(url, headers=headers)
        rep = urllib2.urlopen(req)

        res = rep.read().split('\n')
	l = len(res)

	for i in range(l):
		spl = 0

		#ID
		if "<h2>" in res[i] :
			print u"发表人："
			print res[i+1].decode("utf-8") 
			spl = 1

		#内容
		if 'class="content"' in res[i]:
			print res[i+4].decode("utf-8")

		#评论
		if 'class="main-text"' in res[i]:
			print "评论：",res[i+1].decode("utf-8")
			spl = 2

		#分隔符
		if spl == 1 :
			print "====================================================================="
		if spl == 2 :
			print
			print
		

    except Exception, e:
        print e

getRealAddr_urllib2()