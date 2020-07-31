from bs4 import BeautifulSoup
import requests
import re

res = requests.get("https://www.taobao.com/")
soup = BeautifulSoup(res.text, 'lxml')

str = "imgHuilanMediaArray.push({'src':'/gdmuseum/_300746/_300758/tc45/515013/2018120709163868233.jpg','title':'A"
#".*?'src':'(.*?\.jpg)','title'"
temp = re.findall(".*?/gdmuseum/./././(\d*)\.jpg'", str)

print(temp)
index_start = str.find("/gdmuseum/")
index_end = str.find(",'title'")

print(index_start,index_end)