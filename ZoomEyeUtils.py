#!/usr/bin/python
# coding:utf-8

'''
ZoomEye查询工具
reference：https://www.zoomeye.org/doc
注意：ZoomEye一般用户有查询数量限制每个月10w条记录
查询可选的参数：
主机设备搜索过滤器
名称	类型	说明	示例
app	string	应用，产品	app: ProFTD
ver	string	版本	ver:2.1
device	string	设备类型	device:router
os	string	操作系统	os:windows
service	string	服务类型	service:http
ip	string	IP 地址	ip:192.168.1.1
cidr	string	CIDR 格式地址	cidr:192.168.1.1/24
hostname	string	主机名称	hostname:google.com
port	string	端口号	port:80
city	string	城市名称	city:beijing
country	string	国家名称	country:china
asn	integer	ASN 号码	asn:8978
Web 应用搜索过滤器
名称	类型	说明	示例
app	string	Web 应用信息	webapp:wordpress
header	string	HTTP headers	header:server
keywords	string	meta 属性关键词	keywords:baidu.com
desc	string	HTTP description 属性	desc:hello
title	string	HTTP Title 标题信息	title: baidu
ip	string	IP 地址	ip:192.168.1.1
site	string	site 搜索	site:baidu.com
city	string	城市名称	city:beijing
country	string	国家名称	country:china
'''

import os
import requests
import json
from urllib import parse
from com.dbc.pybaseproj.utils.FileUtil import FileUtil


class ZoomEyeUtils(object):
    '''
    定义基本参数
    '''
    # access_token文件保存路径
    tokenfile = '/Users/dabaicai/Documents/Security/Info/zoomeye_token.txt'
    # login_url
    login_url = 'https://api.zoomeye.org/user/login'
    # searchApp_url
    searchApp_url = 'https://api.zoomeye.org/host/search?'
    # token-登录后每次访问需要带上
    access_token = ''
    # headers
    headers = {}
    # 查询条件
    search_params = {}
    # 结果列表
    ip_list = []

    """
    登录方法
    """

    def login(self):
        username = input('[-] input : username :')
        passwd = input('[-] input : password :')
        # 登录用的数据字典参数
        data = {
            'username': username,
            'password': passwd
        }
        # 转化为JSON
        data_json = json.dumps(data)
        try:
            response = requests.post(url=self.login_url, data=data_json)
            response_decode = json.loads(response.text)
            self.access_token = response_decode['access_token']
            # 将access_token写入文件，供后续一段时间使用
            FileUtil.writeDataFile(self.tokenfile, 'w', self.access_token)
            # print(self.access_token)
        except Exception as e:
            print('[-] info : username or password is wrong, please try again ')
            exit()

    def login(self, username, passwd):
        # 登录用的数据字典参数
        data = {
            'username': username,
            'password': passwd
        }
        # 转化为JSON
        data_json = json.dumps(data)
        try:
            response = requests.post(url=self.login_url, data=data_json)
            response_decode = json.loads(response.text)
            self.access_token = response_decode['access_token']
            # 将access_token写入文件，供后续一段时间使用
            FileUtil.writeDataFile(self.tokenfile, 'w', self.access_token)
            # print(self.access_token)
        except Exception as e:
            print('[-] info : username or password is wrong, please try again ')
            exit()

    '''
    curl -X GET 'https://api.zoomeye.org/host/search?query=port:21%20city:beijing&page=1&facets=app,os' \
-H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5..."
    '''

    def buildQueryString(self, paramValues):
        data = parse.urlencode(paramValues).encode('utf-8')
        print(data)

    def searchApp(self, queryParams):
        """
        查找特定应用程序
        """
        # 显示页数
        page = 1
        if self.access_token is None or self.access_token == '':
            # 从文件读取token
            self.access_token = FileUtil.readDataFile(self.tokenfile, 'r')
        # 初始化headers
        self.headers = {
            'Authorization': 'JWT ' + self.access_token
        }
        self.search_params = queryParams
        try:
            response = requests.get(url=self.searchApp_url, headers=self.headers, params=self.search_params)
            response_decode = json.loads(response.text)
            # 处理匹配的结果
            for match_item in response_decode['matches']:
                self.ip_list.append(match_item['ip'])
            #print(self.ip_list)
        except Exception as e:
            print('[-] info : ' + str(e.message))
        return self.ip_list

    def queryMemcached(self):
        queryParams = {
            'query': '+app:"Memcached"',
            'page': 1
        }
        self.login()
        return self.searchApp(queryParams)


if __name__ == '__main__':
    # app:"memcached" +country:"CN"
    queryParams = {
        'query': 'app:"memcached" +country:"CN"',
        'page': 1
    }
    zoomEyeUtils = ZoomEyeUtils()
    zoomEyeUtils.login("dxbaicai@outlook.com", "5d.QjM_WBLHL")
    target_list = zoomEyeUtils.searchApp(queryParams)
    print(target_list)
