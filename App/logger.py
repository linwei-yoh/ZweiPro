#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

# format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
def logconfig():
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='ErrMsg.log',
                        filemode='a+')
    
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('msg').addHandler(console)


logconfig()
logger = logging.getLogger('msg')

if __name__ == '__main__':
    logger.error("报错测试")
