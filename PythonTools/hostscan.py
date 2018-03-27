#!/usr/bin/python
#coding:utf-8

import commands
from threading import Thread
from optparse  import OptionParser

usage      = "Usage: %prog -q(quickly) -r <range> -a(alive) -p <ipprefix>"
quickHelp  = "Open more thread to speed up the scan speed"
activeHelp = "Only show the hosts which is alive"
rangeHelp  = "special a range to scan ip list"
prefixHelp = "special a prefix for a ip address, default: 192.168.10."


parser = OptionParser(usage = usage)

parser.add_option("-q", action="store_true", dest="quickmode", help=quickHelp)
parser.add_option("-a", action="store_true", dest="activeOnly", help=activeHelp)
parser.add_option("-r", type="string", dest="range", help=rangeHelp)
parser.add_option("-p", type="string", dest="prefix", help=prefixHelp)

(options, args) = parser.parse_args()



def doPing(ipaddr):
    pingCommand = "ping " + ipaddr + " -W 1 -c 2 | grep icmp_seq "
    code, res = commands.getstatusoutput(pingCommand)
    if "icmp_seq" in res:
        print ipaddr + ": alive"
    else :
        if options.activeOnly != True: 
            print ipaddr + ": down"


def main():
    if options.prefix: 
        ipprefix = options.prefix
    else:
        ipprefix = "192.168.10."

    if options.range:
        start = options.range.split("-")[0]
        stop  = options.range.split("-")[1]
    else:
        start,stop = 100,200

    
    for i in range( int(start) , int(stop)):
        ipaddr = ipprefix + str(i)
        if options.quickmode :
            t = Thread(target=doPing, args=(ipaddr,))
            t.start()
        else:
            doPing(ipaddr)



if __name__ == "__main__":
    main()

