#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def getBsObjFromUrl(url):
    try:
        r = requests.get(url, timeout=5)
    except (requests.ConnectionError, requests.HTTPError) as e:
        print("页面获取出错 %s", url)
        return None
    else:
        bsObj = BeautifulSoup(r.text, 'lxml')
        r.close()
        return bsObj


if __name__ == '__main__':
    pass
