import nmap
import optparse



def osscan(host):
	scanner = nmap.PortScanner()
	results = scanner.scan(hosts=host, arguments='-O')
	res = results['scan'].values()
	print res[host]['osmatch'][0]['name']



def main():  
	parser = optparse.OptionParser('usage%prog '+'-H <target host>')  
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')  
	(options, args) = parser.parse_args()  
	host = options.tgtHost  
	if host == None:  
		print parser.usage  
		exit(0)
	osscan(host)
	
if __name__ == '__main__':
	main()
