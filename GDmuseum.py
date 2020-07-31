# coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup as bs

host = 'http://www.gdmuseum.com/'

URL = 'http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/index.html'

ROOT = "广东博物馆"


def safe_string(_string):
    return re.sub('[:,.\'&%$@!~*；‘：&……%￥#]', '_', _string)


def DownImage(image_url) -> None:
    image_res = requests.get(image_url)

    string_str = image_res.text
    temp = re.findall(".*?'src':'(.*?\.jpg)','title'", string_str)
    image_url = f'{host}{temp[0]}'
    soup = bs(image_res.text, 'lxml')
    # print(soup.select('.js_title')[0].p.text)
    image_name = soup.select('.js_title')[0].p.text
    download_comic(image_url, image_name)


def download_comic(comic_url, comic_name, *args, **kwargs) -> None:
    _path_1 = os.sep.join([ROOT, safe_string(comic_name)])
    print(_path_1)
    if not os.path.exists(_path_1):
        os.makedirs(_path_1)
    response = requests.get(comic_url)
    file_pth = _path_1+"/"+comic_name+'.jpg'
    with open(file_pth, 'wb') as f:
        f.write(response.content)
        print(f'<{comic_name}> 下载成功~')

def GetImage(url):
    res = requests.get(url)

    soup = bs(res.text, 'lxml')

    parent = soup.select('.js_cont')[0].select('.js_img')

    for item in parent:
        path = item.select('.pro_img')[0]['href']
        image_url = f'{host}{path}'
        DownImage(image_url)


if __name__ == '__main__':
    GetImage(URL)
