import os
import random
import time
import requests
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OSX10_14_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
xpath='//*[@id="big-pic"]/p/a/img/@src'

def fetch(url,xpath):
    resp=requests.get(url,headers=headers)
    html=etree.HTML(resp.text)
    urls=html.xpath(xpath)
    return urls
def create(filename):
    if not os.path.exists('%s'%filename):
        os.mkdir('%s'%filename)
    os.chdir('%s'%filename)
def writ(images_url):
    global i
    for url in images_url:
        time.sleep(random.randint(0,2))
        file_name="%s%d.jpg"%(filename,i)
        res=requests.get(url,headers=headers)
        with open(file_name, 'wb') as f:
            f.write(res.content)
        i+=1
        print(url)
home_url='http://www.mmonly.cc/tag/xy/'
links=fetch(home_url,'//*[@id="infinite_scroll"]/div/div[1]/div/div[1]/a/@href')
for url1 in links:
    next=''
    filename=fetch(url1,'/html/body/div[2]/div[2]/div[2]/h1/text()')[0]
    filename=filename.encode('iso-8859-1').decode('gbk')
    create(filename)
    i=0
    while next!="##":
        images_url=fetch(url1,xpath)
        next=fetch(url1,'//*[@id="nl"]/a/@href')[0]
        url1=url1.replace(url1.split('/')[-1],next)
        writ(images_url)
    os.chdir(os.path.abspath(os.path.dirname(os.getcwd())))
