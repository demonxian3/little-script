import sys
from threading import Thread
from scapy.all import *

if len(sys.argv) < 2:
    print "please input interface"
    sys.exit()

def mping(ipaddr):
    pkt =  IP(dst=ipaddr.strip()) /ICMP();
    res = sr1(pkt, timeout=1, verbose=0);
    if res:
        print ipaddr + " is alive";


ip = get_if_addr(sys.argv[1]);
iparr = ip.split('.');
prefix = iparr[0] + '.' + iparr[1] + '.' + iparr[2] + '.';
print prefix


for i in range(1,255):
    ipaddr = prefix + str(i);
    t = Thread(target=mping, args=(ipaddr,))
    t.start()
