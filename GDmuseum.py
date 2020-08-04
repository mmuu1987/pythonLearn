# coding:utf-8
from typing import TextIO

import requests
import re
import os
from bs4 import BeautifulSoup as bs

host = 'http://www.gdmuseum.com/'

URL = 'http://www.gdmuseum.com/gdmuseum/_300746/index.html'

ROOT = "广东博物馆"

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

Secondir = ''

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36'}




def safe_string(_string):
    return re.sub('[:,.\'&%$@!~*；‘：&……%￥#]', '_', _string)


def DownImage(image_url) -> None:
    try:
        image_res = requests.get(image_url,proxies=proxies)
        string_str = image_res.text
        temp = re.findall(".*?'src':'(.*?\.jpg)','title'", string_str)
        image_url = f'{host}{temp[0]}'
        soup = bs(image_res.text, 'lxml')
        # print(soup.select('.js_title')[0].p.text)
        image_name = soup.select('.js_title')[0].p.text
        des = soup.select('.cp_list dl')[0].select('dd')
        detect = ''
        for desire in des:
            # 去掉回车换行符
            detect += desire.text.replace("\r", "").replace("\n", "").strip() + '\r\n'
        download_comic(image_url, image_name, detect)
    except Exception as e:
        print(f' 图片 {image_url} 下载失败：{e}')


def download_comic(comic_url, comic_name, *args, **kwargs) -> None:
    _path_1 = os.sep.join([Secondir, safe_string(comic_name)])
    print(_path_1)
    if not os.path.exists(_path_1):
        os.makedirs(_path_1)
    print("需要下载的链接地址是： " + comic_url)

    file_despath = _path_1 + '/' + comic_name + ".txt"
    if not (os.path.exists(file_despath)):
        with open(file_despath, 'w+', encoding='utf-8') as f:
            f.write(args[0])
            print(f'{comic_name}  描述文件下载成功')

    file_pth = _path_1 + "/" + comic_name + '.jpg'
    if os.path.exists(file_pth):
        return
    response = requests.get(comic_url, headers=headers,proxies=proxies)
    with open(file_pth, 'wb') as f:
        f.write(response.content)
        print(f'<{comic_name}> 下载成功~')


# 遍历展品下载--------- 3
def GetImage(url, exhibits):
    path = os.sep.join([ROOT, safe_string(exhibits)])
    global Secondir
    Secondir = path
    if not os.path.exists(path):
        os.makedirs(path)
    res = requests.get(url, headers=headers,proxies=proxies)

    soup = bs(res.text, 'lxml')

    parent = soup.select('.js_cont')[0].select('.js_img')

    for item in parent:
        path = item.select('.pro_img')[0]['href']
        image_url = f'{host}{path}'
        print("GetImage   " + image_url)
        DownImage(image_url)


# 获取每个展品类的URL--------- 1
def GetURL():
    res = requests.get(URL, headers=headers, proxies=proxies)
    soup = bs(res.text, 'lxml')
    list_item = soup.select('div .product')

    n = 0
    for item in list_item:
        if n <= 1:
            n += 1
            continue
        href = item.select('.product_img')[0]['href']
        # 排除选项
        if 'http://' in str(href):
            continue
        else:
            print(host + href)
            exhibits = item.select('.product_title')[0].select('.name')[0].text.strip()
            #  GetImage(host + href, exhibits)
            GetEveryPage(href, exhibits)



# 解析展品每页的url--------- 2
def GetEveryPage(url, exhibits):
    res = requests.get(host + url, headers=headers,proxies=proxies)
    temp = re.findall(".queryArticleByCondition\(this,'(.*?\.html)'\)\" class", res.text)
    temp.append(url)
    for item in temp:
        image_url = f'{host}{item}'
        print(image_url)
        GetImage(image_url, exhibits)


if __name__ == '__main__':
    GetURL()
