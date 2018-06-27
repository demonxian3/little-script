import socket
import time
from scapy.all import *
import optparse


def tcpconnscan(host,port):
	try:
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.connect((host,port))
		print '[+]%d/tcp open'% port
		conn.close()
	except:
		pass

     
def udpconnscan(host,port):
	try:
		rep = sr1(IP(dst=host)/UDP(dport=port), timeout=1, verbose=0)
		time.sleep(1)
		if (rep.haslayer(ICMP)):
			print '[-]%d/udp not open'% port
	except:
		print '[+]%d/udp open'% port


		
def portscan(host):
	for port in range(1,1023):
		tcpconnscan(host,port)



def main():  
	parser = optparse.OptionParser('usage%prog '+'-H <target host>')  
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')  
	(options, args) = parser.parse_args() 
	host = options.tgtHost
	if host == None:  
		print parser.usage  
		exit(0)
	portscan(host)


	
if __name__ == '__main__':
	main()
