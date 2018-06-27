# coding: utf-8
# author: Demon, Demonxian3
# date:   2018-04-05
# desc:   Show TCP connection's information

import sys
import os
import urllib  
import urllib2  
import httplib

from time import sleep



#  ***********************************************************************
#  **				  My Function 			        **
#  ***********************************************************************

'''   此处使用urllib 模块 发送POST请求给 chinaz '''
def getRealAddr_urllib2(ip):
    try:
        url="http://ip.chinaz.com"
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        params = {'ip' : ip}

        data = urllib.urlencode(params)

        req = urllib2.Request(url, data, headers)
        rep = urllib2.urlopen(req)

        res = rep.read().split("\n")

        first = 0
        for i in res:
            if "Whwtdhalf w50-0" in i and "IP" not in i:
                address =  i.split(">")[1].split("<")[0].decode("utf-8").encode("gb2312")

        return address

    except Exception, e:
        print e
	return "暂查不到地址"





'''   此处使用httplib 模块 发送POST请求给 ipchinaz  '''
def getRealAddr_httplib(ip):
    httpClient = None
    try:
        params = urllib.urlencode({'ip': ip})
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        httpClient = httplib.HTTPConnection('ip.chinaz.com', 80, timeout=3)
        httpClient.request('POST', '/34.213.135.138', params, headers)
        response = httpClient.getresponse()
    
        body = response.read().split("\n")

        for i in body:
            if "Whwtdhalf w50-0" in i and "IP" not in i:
                address =  i.split(">")[1].split("<")[0].decode("utf-8").encode("gb2312")

        httpClient.close()
        return address

    except Exception, e:
        print e
        httpClient.close()
	return "暂查不到地址"

            

#  ***********************************************************************
#  **				  Main flow 			        **
#  ***********************************************************************


#netstat#
filter_unTCP =    'find    "TCP"'
filter_local =    'find /v "127.0.0.1"'
filter_internet = 'find /v "0.0.0.0"'
filter_ipv6 =     'find /v "*:*" | find /v "[::]"'

cmd_netstat  = 'netstat -ano|' + filter_local+'|'+filter_internet+'|'+filter_ipv6+'|'+filter_unTCP
print  cmd_netstat
p = os.popen(cmd_netstat)
connections = p.read().split("\n")

print "src\t\t    dst\t\t\tprogram\t\taddress"
for conn in connections:
    try:
        myNet = []
        res = conn.strip("\n")
        myNet = res.split("    ")
        try:
            myNet.remove("")
        except:
            pass
        
        src   = myNet[1].strip(" ");
        dst   = myNet[2].strip(" ");
        pid   = myNet[4].strip(" ");
        
        
        
        #tasklist#
        cmd_tasklist = 'tasklist | find /i "'+ pid +'"'
        p = os.popen(cmd_tasklist)
        res = p.readline()
        process = res.split(" ")[0]
        
        ipaddr = dst.split(":")[0]
        realAddr = getRealAddr_urllib2(ipaddr)
        
        
        
        #result#
        print src + "  " + dst + "  " + process + ":" + pid + "  " + realAddr
    except:
        pass
