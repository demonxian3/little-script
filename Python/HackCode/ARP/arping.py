#!/usr/bin/python
#coding:utf-8
#author:demon
#date:2018-05-04

from scapy.all import *
import sys

try:
    ip = sys.argv[1]
    print sr1(ARP(pdst=ip), verbose=0, timeout=1).psrc + " is alive"
except:
    print "missing params or error happened"
