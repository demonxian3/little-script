#coding: utf-8

import sys
import os
import urllib  
import urllib2  
import httplib
import re
import time
from bs4 import BeautifulSoup

industry_code = {}

def httpGo(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(req, timeout = 5)



def getCode():
    url="http://q.10jqka.com.cn/thshy/";
    rep = httpGo(url);
    res=  rep.read().split("\n");

    for line in res:
        if "td" in line:
            continue

        if "<a href=" in line:
            matchObj = re.match(r".*code.*(\d{6}).*>(.*)<", line);
            if matchObj and matchObj.group(2) :
                try:
                    code = int(matchObj.group(1))
                    name = matchObj.group(2).decode("gb2312").encode("utf-8");
                    #print  line.decode("gb2312").encode("utf-8"),
                    #print name
                    industry_code[code]  = name
                except:
                    pass





def createDir():
    for i in industry_code:
        dirname = industry_code[i]
        if not os.path.exists(dirname):
            os.system("mkdir " + dirname)




def crawlTitle():
    for code in industry_code:
        #print "准备爬取 " + industry_code[code] +" 行业的所有文章";
        time.sleep(1)
        dirname = industry_code[code];
        url = "http://news.10jqka.com.cn/list/field/"+str(code)+"/index_1.shtml"
        crawlContent(url, dirname)
        url = "http://news.10jqka.com.cn/list/field/"+str(code)+"/index_2.shtml"
        crawlContent(url, dirname)
        url = "http://news.10jqka.com.cn/list/field/"+str(code)+"/index_3.shtml"
        crawlContent(url, dirname)




def crawlContent(url, dirname):
        rep = httpGo(url);
        res = rep.read().split("\n");

        alink = 0
        #遍历每个行业的文章首页 遍历三页
        for line in res:

            if 'arc-title' in line:
                alink = 1
                continue

            if alink:
                alink = 0

                matchObj = re.match(r'.*title="(.*?)".*href="(.*?)"', line);
                if matchObj:
                    try:
                        titleName = matchObj.group(1).decode("gb2312").encode("utf-8")
                        linkName = matchObj.group(2)
                        storageToFile(dirname, titleName, linkName);
                    except:
                        print "Cannot decode titleName" + titleName
                        pass



def storageToFile(dirname, titleName, linkName):
    print "准备爬取" + titleName + "文章" 
    filepath = dirname + "/"+titleName+".txt"

    if os.path.exists(filepath):
        return 
    #time.sleep(1)
    if os.path.exists(dirname):
        try:

            print "\033[31m\t\t" + linkName + "\033[0m\t\t\t"
            response = urllib2.urlopen(linkName ,timeout = 5)
            
            soup = BeautifulSoup(response, 'lxml')
            items = soup.select("h2.main-title")
            title = items[0].get_text()
            
            print "\033[31m\t\t" + title + "\033[0m\t\t"
            
            items = soup.select("div.main-text.atc-content > p")
            content =  ''
            
            for item in items:
                bottom = item.get("class")
                if bottom is not None and "bottomSign" in bottom:
                    break
                content += item.get_text() +"\n"
            
            
            #save content to the file, filename is titlename
            fp = open(filepath, "w");
            fp.write(content.encode("utf-8"))
            fp.close()
        except:
            pass

    else:
        print  dirname + "目录不存在"

    
        

getCode()
createDir()
crawlTitle()

