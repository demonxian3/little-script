#!/usr/bin/python
#coding:utf-8

import sys
import socket

from color      import printColor
from threading  import Thread
from optparse   import OptionParser

socket.setdefaulttimeout(1)

usage = "Usage: %prog -f <filename>  -p <prefix>  -r <range>  -e <show no banner> -t <quick>"
parser = OptionParser(usage = usage) 
parser.add_option("-f", "--filename",type="string", dest="filename",help = "file of ipaddress, like: ip.txt")
parser.add_option("-r", "--range",   type="string", dest="range",   help = "range of ipaddress, like: 100-200")
parser.add_option("-p", "--prefix",  type="string", dest="prefix",  help = "prefix of ipaddress, like: 192.168.10.")
parser.add_option("-t", "--thread",  action="store_true", dest="thread",  help = "run program with multi thread")
parser.add_option("-e", "--error",   action="store_true", dest="error")

(options, args) = parser.parse_args()

'''*************Help*************'''
if options.range == None and options.filename == None:
    parser.error("must select -f or -r ")
'''******************************'''



def readIPFile():
    try:
        f = open(options.filename, "r")
        ipaddrs = f.read()
        f.close()
        return ipaddrs.split("\n")
    except Exception, e:
        print e
        sys.exit(1)




def getBanner(ip, port):
    s = socket.socket()
    try:
        s.connect((ip, port))
        banner = s.recv(1024)
        s.close()
        return banner
    except:
        return



def printStatus(ip,code):
    if code == 1:
        printColor("success", ip+":vulnerable")
    if code == 0:
        printColor("warning", ip+":unvulnerable")
    if code == -1 and options.error:
        printColor("danger", ip+":no banner")




def checkVulns(ip, port):
        # check banner if has keyword "2.3.4" for vsftpd
        status = [-2]
        banner = getBanner(ip, port)
        if banner:
            if("2.3.4" in banner):
                status[0] = 1
            else:
                status[0] = 0
        else:
            status[0] = -1
        printStatus(ip, status[0])




''' is dependent on runing '''
def main(): 
    if options.prefix != None:
        ipprefix = options.prefix
    else:
        ipprefix =  "192.168.10."

    port = 21


    if options.range != None:
        start = options.range.split("-")[0]
        stop  = options.range.split("-")[1]
        for i in range(int(start), int(stop)):
            ipaddr = ipprefix + str(i)
            if options.thread:
                t = Thread(target = checkVulns, args=(ipaddr, port))
                t.start()
            else:
                checkVulns(ipaddr, port)


    if options.filename != None:
        iplist = readIPFile()
        if iplist:
            for ipaddr in iplist:
                if options.thread:
                    t = Thread(target=checkVulns, args=(ipaddr,port))
                    t.start()   
                else:
                    checkVulns(ipaddr, port)



if __name__ == "__main__":
    main()


