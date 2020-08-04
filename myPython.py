from bs4 import BeautifulSoup
import requests
import re

# res = requests.get("https://www.taobao.com/")
# soup = BeautifulSoup(res.text, 'lxml')
#
# str = "imgHuilanMediaArray.push({'src':'/gdmuseum/_300746/_300758/tc45/515013/2018120709163868233.jpg','title':'A"
# #".*?'src':'(.*?\.jpg)','title'"
# temp = re.findall(".*?/gdmuseum/./././(\d*)\.jpg'", str)
#
# print(temp)
# index_start = str.find("/gdmuseum/")
# index_end = str.find(",'title'")
#
# print(index_start,index_end)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用requests请求代理服务器
请求http和https网页均适用
"""

import requests

# 提取代理API接口，获取1个代理IP
api_url = "http://dps.kdlapi.com/api/getdps/?orderid=969644583558638&num=1&pt=1&sep=1"

# 获取API接口返回的代理IP
proxy_ip = requests.get(api_url).text

# 用户名密码方式
username = "744845918"
password = "awdn0fzm"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
}
# 要访问的目标网页
target_url = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/dy/index.html"

# 使用代理IP发送请求
response = requests.get(target_url, proxies=proxies)

# 获取页面内容

print(response.text)