#!/usr/bin/python3
#coding=utf-8

'''
Author: matiastang
Date: 2023-07-12 15:29:25
LastEditors: matiastang
LastEditTime: 2023-07-12 16:33:16
FilePath: /matias-TensorFlow/src/welfareLottery/utils/transform.py
Description: transform util
'''

import doctest
from typing import List
import logging  
logging.basicConfig(level=logging.WARN)  

def transformReds(reds: str) -> List[int]:
    '''
    逗号分割的数字字符串转换为数组
    >>> transformReds('03,04,15,18,19,22')
    [3, 4, 15, 18, 19, 22]
    >>> transformReds('13,15,24,28,30,31')
    [13, 15, 24, 28, 30, 31]
    >>> transformReds('')
    []
    >>> transformReds('03-04')
    []
    '''
    try:
        # 分割
        strList = reds.split(',')
        # 过滤
        filterList = list(filter(lambda item: item, strList))
        # 判断
        if len(filterList) <= 0:
            return []
        # 转换
        return [int(item) for item in filterList]
    except ValueError as e:
        return []
    except Exception as e:
        logging.warn('发生异常:', e)
        return []

def main():
    print(__file__, 'doctest')  
    doctest.testmod()
      
if __name__ == "__main__":  
    main()