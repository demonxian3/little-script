from scapy.all import *
import optparse
from threading import *
#Flag1=scapy.optparse.threading


def sweep(packet):
	try:
		reply = srp1(packet,timeout = 1,verbose = 0,iface = 'eth0')
		print 'IP:' + reply.psrc + '   MAC:' + reply.hwsrc

	except:
		pass

#Flag2=F4.F5.F6
#sweep.psrc.hwsrc
	
def main():  
	parser = optparse.OptionParser('usage%prog '+'-H <target host segment/eg:(192.168.1.)>')  
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host segment/eg:(192.168.1.)')  
	(options, args) = parser.parse_args()  
	host = options.tgtHost
	if host == None:   
		print parser.usage  
		exit(0)
	#Flag3=F7.F8.F9
	eth = Ether()
	eth.dst = 'ff:ff:ff:ff:ff:ff'
	eth.type = 0x0806
	arp = ARP()
	#Flag4=F10.F11.F12
	for n in range(1,254):
		arp.pdst = host + str(n)
		packet = eth/arp
		t = Thread(target = sweep, args = (packet))
		t.start()
		
#Flag3=parser.options.host
#Flag4=Ether.dst.type

	
if __name__ == '__main__':
	main()

#Flag5=F13.F14.F15
#Flag5=pdst.packet.t
