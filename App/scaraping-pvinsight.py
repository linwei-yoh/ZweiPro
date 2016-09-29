#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Disallow: /Data/
# Disallow: /Price/
# Disallow: /PriceDownLoad/
# Disallow: /PolySilicon/
# Disallow: /SolarWafer/
# Disallow: /SolarCell/
# Disallow: /SolarModule/

savaPath = '../PVinsightData'

if __name__ == '__main__':
    if not os.path.exists(savaPath):
        os.makedirs(savaPath)
