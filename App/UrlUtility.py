#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose


def getBsObjFromUrl(url, s=None):
    hreader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.112 '
                             'Safari/537.36'}
    count = 0
    while 1:
        try:
            if s is None:
                result = requests.get(url, headers=hreader, timeout=5)
            else:
                result = s.get(url, headers=hreader, timeout=5)
        except (requests.ConnectionError, requests.HTTPError) as e:
            count += 1
            if count > 5:
                print("页面获取出错 %s", url)
                return None
        else:
            break

    bsObj = BeautifulSoup(result.text.encode(result.encoding).decode('utf-8'), 'lxml')
    result.close()
    return bsObj


if __name__ == '__main__':
    pass
