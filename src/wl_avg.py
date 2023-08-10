#!/usr/bin/python3
#coding=utf-8

'''
Author: matiastang
Date: 2023-07-06 11:14:59
LastEditors: matiastang
LastEditTime: 2023-08-10 09:54:46
FilePath: /matias-TensorFlow/src/welfareLottery/wl_avg.py
Description: 
'''

from typing import List, Dict, Union
import pymysql
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from utils.transform import transformReds
import logging  
logging.basicConfig(level=logging.ERROR)
print(mpl.__version__)
# plt.rcParams['font.family'] = 'sans-serif'  # 设置中文字体  
# plt.rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号乱码问题

# from matplotlib.font_manager import FontProperties 

# mpl.rcParams['font.family'] = ['PingFang TC']  
# mpl.rcParams['font.sans-serif'] = ['PingFang TC']  
# mpl.rcParams['font.monospace'] = ['PingFang TC']  
# mpl.rcParams['font.serif'] = ['PingFang TC']  
# mpl.rcParams['font.cursive'] = ['PingFang TC']  
# mpl.rcParams['font.fantasy'] = ['PingFang TC']

import matplotlib.font_manager as font_manager
  
# 重新构建字体列表  
# font_manager._rebuild()
print('font_filename=====start')
# 打印所有可用字体  
for font_filename in font_manager.fontManager.ttflist:  
    print(font_filename)
print('font_filename=====end')



def view_fonts(fs):  
    mpl.rcParams['font.family'] = fs  
    fs = mpl.font_manager.FontProperties(family=fs)  
    mpl.rcParams['font.size'] = fs.get_size()  
    print("Available fonts:")  
    for font in mpl.font_manager.get_fontconfig_fonts():  
        if 'DejaVu Sans' in font:  
            print(font)
# view_fonts('DejaVu Sans')

def welfareLotteryAvgLine(dates: List[int], reds: List[int]):
    # 画布
    plt.figure(figsize=(100,5))
    plt.plot(dates, [i for i in reds], label = 'red svg')
    # plt.rcParams['font.family']='PingFang TC'  #设置字体，默认字体显示不了中文
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
    print(plt.rcParams)
    # 设置图表标题
    plt.title('svg line')
    # x轴标题
    plt.xlabel('code')
    # y轴标题
    plt.ylabel('svg')
    # y轴范围
    plt.ylim(1, 33)
    # 显示
    plt.show()

# 链接mysql
connect = pymysql.connect(
    host='127.0.0.1',
    # host='110.41.145.30',
    db="mt_scrapy",
    user="root",
    # user='matiastang',
    passwd="MySQL_18380449615",
    charset='utf8',
    use_unicode=True,
    cursorclass=pymysql.cursors.DictCursor
)
# 通过cursor执行增删查改
cursor = connect.cursor()

data: List[Dict[str, Union[str, int, List[int]]]] = []

try:
    # sql
    sql = """
        SELECT * from welfare_lottery_double ORDER BY code DESC LIMIT 20;
    """
    # 查询
    cursor.execute(sql)
    # 获取
    result=cursor.fetchall()
    # 聚合
    data = [{'code': item['code'], 'date': item['date'], 'blue': int(item['blue']), 'reds': transformReds(item['red']) } for item in result]
    
except Exception as e:
    logging.error(e)
    connect.rollback()
    
date = [item['date'] for item in data]
dateReds = [np.mean(item['reds']) for item in data]
# welfareLotteryAvgLine(date[:10], dateReds[:10])
# welfareLotteryAvgLine(date, dateReds)

# 退出
connect.close()
cursor.close()