import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
s.bind(('', 6000));

while 1:
    data, addr = s.recvfrom(1024);
    print "connect: " + str(addr) +"\nRecv: "+ str(data)
    s.sendto(data,addr)
s.close()
