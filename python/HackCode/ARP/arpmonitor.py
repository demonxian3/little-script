#!/usr/bin/python
#coding: utf-8

from scapy.all import sniff,ARP
from signal import signal,SIGINT
import sys

ip_mac = {}

def  watchArp(pkt):
    global ip_mac;
    if pkt[ARP].op == 2:
        print "[r] ", pkt[ARP].psrc + "\t\t", pkt[ARP].hwsrc;

    if ip_mac.get(pkt[ARP].psrc) == None:
        print "[+] ", pkt[ARP].psrc + "\t\t", pkt[ARP].hwsrc;
        ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc;

    elif ip_mac[pkt[ARP].psrc] != pkt[ARP].hwsrc :
        print "[u] ", pkt[ARP].psrc + "\t\t", pkt[ARP].hwsrc;
        ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc;



sniff(iface='eth0', filter='arp', store=0, prn=watchArp);
