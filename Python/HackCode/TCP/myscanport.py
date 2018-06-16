#coding: utf-8
#FIN 1
#SYN 2
#RST 4
#ACK 16
# 如果对方端口在线， 返回ack + syn     "SA" 16 + 2 = 18
# 如果对方端口不在线， 返回 ack + rst  "RA" 16 + 4 = 20

import sys
from scapy.all import *
from threading import Thread


if len(sys.argv) < 2:
    sys.exit();

ip = sys.argv[1];

def tcpPortScan(port):
    try:
        pkt = IP(dst=ip) /  TCP(dport=port, flags='S');
        res = sr1(pkt, timeout=1, verbose=0);
        if res and res[TCP].flags == 18:
            print ip + ":"+ str(port) + " is open";
    except:
        pass;


for i in range(1,1024):
    t = Thread(target=tcpPortScan, args=(i,));
    t.start()
