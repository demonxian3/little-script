#coding: utf-8
import sys
import socket
from threading import *

ip = sys.argv[1];

def scanport(port):
    try:
        s = socket.socket();
        s.connect((ip, port));
        print ip + ":" + str(port) + " is open";
        s.close();
    except:
        pass


for i in range(1024):
    scanport(i);
