import sys
import time
from scapy.all import *

if len(sys.argv) < 2:
    print "usage: %prog 192.168.10.1 53"
    sys.exit();

ip = sys.argv[1];
res = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0 );

if not res:
    print ip + " is down";



def udpPortScan(port):
    pkt = IP(dst=ip) / UDP(dport=port);
    res = sr1(pkt, timeout=3, verbose=0);
    time.sleep(1)
    if res and res[ICMP]:
        print ip + ":" + str(port) +" is down";
    else:
        print ip + ":" + str(port) +" is open";



for i in [53, 80, 3389, 500, 5333, 5355, 3700, 3600]:
    udpPortScan(i);
