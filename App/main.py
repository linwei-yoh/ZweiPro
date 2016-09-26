#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.error import HTTPError,URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup


# params = {'firstname':'AL','lastname':'Lin'}
# r = requests.post("http://pythonscraping.com/pages/files/processing.php",data=params)
# print(r.text)

#硅料Index URL
ObjUrl_1 = "http://db.solarzoom.com/price_data/21001/index.htm"

def getPage(url):
    try:
        html = urlopen(url)
    except (HTTPError,URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"lxml")
    except ArithmeticError as e:
        return None
    return bsObj


if __name__ == '__main__':
    html = urlopen(ObjUrl_1)
    bsObj = BeautifulSoup(html, 'lxml')
    formlist = bsObj.find("form",{"id":"listForm"})
    namelist = formlist.findAll("a",{"target":"_blank"})
    
    for item in namelist:
        print(item)
 