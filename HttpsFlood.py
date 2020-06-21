#!/usr/bin/python
# coding:utf-8

'''
1. 指定证书位置
requests.get('https://kennethreitz.org', cert=('/path/client.cert', '/path/client.key'))
2. 设置忽略证书验证
req = requests.get('https://grwsyw.bjgjj.gov.cn/ish/',verify=False)
'''

import ssl



