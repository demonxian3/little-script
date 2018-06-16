#!/usr/bin/python
#coding: utf-8

import sys
import subprocess
from threading import Thread
from scapy.all import *

if len(sys.argv) != 2:
        print "param missing"
        sys.exit()

intf = sys.argv[1]
ip = subprocess.check_output('ifconfig '+intf+ '|grep -w inet| awk \'{print $2}\'', shell=True);
iparr = ip.split('.');
prefix = iparr[0] + "." + iparr[1] + "." + iparr[2] + ".";

def scan(ip):
    try:
        print sr1(ARP(pdst=ip), timeout=2, verbose=0).psrc + " is alive"
    except:
        pass

for i in range(1,254):
    ipaddr = prefix + str(i)
    t = Thread(target=scan, args=(ipaddr,))
    t.start()
