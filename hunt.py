#!/usr/bin/python
# -*- coding=utf-8 -*-
# coding: utf-8

from urllib import request
import bs4
from bs4 import BeautifulSoup

# url='http://cg.17173.com/item/famu.shtml'
url='http://cg.17173.com/item/shoulie.shtml'

fm1=[]
fm2=[]
stuff_list=[]
req = request.Request(url)
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    #破网页用的中文gb2312编码
    soup = BeautifulSoup(f.read().decode('gbk'), "lxml")
    #定位到列表的table
    # soup.prettify()
    stuff = soup('table')[-3]
    
    for td in stuff:
        for at in td:
            if(type(at)==bs4.element.Tag):
                if(len(at)==10):
                    try:
                        if(at.img != None):
                            fm1.append(at)
                    except:
                        continue
                else:
                    try:
                        if(at.div != None and not ('class' in at.div.attrs)):
                            fm2.append(at)
                    except:
                        continue

f = open('hunt.txt','a+', encoding='utf-8')

for i in range(len(fm1)):

    de=fm1[i]
    icon_url=de.img['src']

    tds=de.find_all('td')
    level=tds[0].div.string.strip('\n')
    local=""
    for s in tds[2].strings:
        s=s.strip('\n').strip('\r')
        local += s
    
    r_local=""
    for s in tds[3].strings:
        s=s.strip('\n')
        r_local += s

    price=""
    for s in tds[4].strings:
        s=s.strip('\n')
        price += s
    ds = fm2[i].find_all('td')
    sr=[]
    for t in ds:
        for s in t.strings:
            s=s.strip('\n')
            if(len(s) < 1):
                continue
            sr.append(s)
    
    name=sr[0]
    desc=''
    if(len(sr) > 1):
        desc=sr[1]
    item = {
        "name":name,
        "local":local,
        "r_local":r_local,
        "price":price,
        "level":level,
        "icon_url":icon_url,
        "desc":desc,
        "ext_desc":""
    }
    # stuff.append(item)
    
    print(item)
    f.write(str(item)+'\n')
f.close()
