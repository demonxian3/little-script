#coding: utf-8
import sys
from scapy.all import *

# 指定一个udp端口，如果对方主机在线并且没有开放udp端口服务，对方会回复端口不可达的icmp报文
# 如果对方主机不在线， 或者刚好开了对应的UDP 服务，那么是不会回复任何消息的

if len(sys.argv) < 2:
    sys.exit()

ipaddr = sys.argv[1];

pkt = IP(dst=ipaddr) / UDP(dport=33897)

res = sr1(pkt, timeout=1, verbose=0)

if res and int(res[IP].proto) == 1 :
    print ipaddr + " is alive"
else:
    print ipaddr + " is down"
