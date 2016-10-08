#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

if __name__ == '__main__':
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    df['E'] = ['one', 'one', 'two', 'three', 'four', 'three']
    
    # 加上.copy()可以避免警告 虽然都能正确设置值
    df2 = df.iloc[1:].copy()
    print(df2)
