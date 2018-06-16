import sys
from scapy.all import *


#FIN 1
#SYN 2
#RST 4
#ACK 16

if len(sys.argv) < 2:
    sys.exit()

ip = sys.argv[1].strip()

pkt = IP(dst=ip) / TCP(dport=80, flags=18);
res = sr1(pkt, timeout=1, verbose=0);

if res and res[TCP].flags == 4:
    print  ip + " is alive\n"
else:
    print  ip + " is down\n"
