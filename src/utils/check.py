#!/usr/bin/python3
#coding=utf-8

'''
Author: matiastang
Date: 2023-08-10 15:03:09
LastEditors: matiastang
LastEditTime: 2023-08-10 15:23:18
FilePath: /matias-TensorFlow/src/welfareLottery/utils/check.py
Description: check util
'''

import doctest
from typing import List
import logging  
logging.basicConfig(level=logging.WARN)  

def checkLevelHistory(reds: List[int], blue: int, buyReds: List[int], buyBlue: int) -> int:
    '''
    检查是否中奖及中奖等级0-6
    >>> transformReds([2 5 13 22 27 32], 1, [2 5 13 22 27 32], 1)
    1
    '''
    bingoBlue = blue == buyBlue
    if (len(reds) != 6):
        logging.warn('开奖结果红球位数不够')
    if (len(buyReds) != 6):
        logging.warn('购买红球位数不够')
    bingoRed = 0
    for item in buyReds:
        if item in reds:
            bingoRed += 1
    if bingoBlue == False:
        if bingoRed == 6:
            return 2
        elif bingoRed == 5:
            return 4
        elif bingoRed == 4:
            return 5
        else:
            return 0
    else:
        if bingoRed == 6:
            return 1
        elif bingoRed == 5:
            return 3
        elif bingoRed == 4:
            return 4
        elif bingoRed == 3:
            return 5
        else:
            return 6

def main():
    print(__file__, 'doctest')  
    doctest.testmod()
      
if __name__ == "__main__":  
    main()