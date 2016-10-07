#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def getBsObjFromUrl(url):
    hreader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.112 '
                             'Safari/537.36'}
    count = 0
    while 1:
        try:
            r = requests.get(url, headers=hreader, timeout=10)
        except (requests.ConnectionError, requests.HTTPError) as e:
            count += 1
            if count > 5:
                print("页面获取出错 %s", url)
                return None
        else:
            break
    
    bsObj = BeautifulSoup(r.text.encode(r.encoding).decode('utf-8'), 'lxml')
    r.close()
    return bsObj


if __name__ == '__main__':
    pass
