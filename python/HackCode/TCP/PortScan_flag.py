import Flag1
def portscan():
	for port in range(1, Flag2):
		conn = Flag3(2, 1)
		try:
			conn.connect((Flag4, port))
			print('Port %d Is Open'%port)
			conn.close()
		except:
			pass
		
Flag5()

