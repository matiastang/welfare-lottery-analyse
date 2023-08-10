#!/usr/bin/python3
#coding=utf-8

'''
Author: matiastang
Date: 2023-07-06 11:14:59
LastEditors: matiastang
LastEditTime: 2023-08-10 16:04:26
FilePath: /matias-TensorFlow/src/welfareLottery/wl_ratio.py
Description: 比例
'''

from typing import List, Dict, Union
import pymysql
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from utils.transform import transformReds
from utils.check import checkLevelHistory
import logging  
logging.basicConfig(level=logging.ERROR)

print(mpl.__version__)

mpl.rcParams['font.family'] = ['Hiragino Sans'] 

# import matplotlib.font_manager as font_manager
# # 打印所有可用字体  
# for font_filename in font_manager.fontManager.ttflist:  
#     print(font_filename)

# def view_fonts(fs):  
#     mpl.rcParams['font.family'] = fs  
#     fs = mpl.font_manager.FontProperties(family=fs)  
#     mpl.rcParams['font.size'] = fs.get_size()  
#     print("Available fonts:")  
#     for font in mpl.font_manager.get_fontconfig_fonts():  
#         if 'DejaVu Sans' in font:  
#             print(font)
# view_fonts('DejaVu Sans')

# 显示饼图
def welfareLotteryRatioPie(data: List[int], range: List[int]):
    # 标签名称
    # labels = list(map(lambda i: str(i) if i >= 10 else ('0' + str(i)), range(1, 17)))
    # labels = [(str(v) if v >= 10 else ('0' + str(v))) for v in range(1, 34)]
    labels = [(str(v) if v >= 10 else ('0' + str(v))) for v in range]
    # 标签数据
    sizes = [data.count(v) for v in range]
    # 设置
    plt.pie(sizes, pctdistance=1.5, labels=labels, radius=1, 
            autopct='%1.3f%%', shadow=False, startangle=90,wedgeprops=dict(width=0.3, edgecolor='w'))
    # 显示
    plt.show()

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
    # sql = """
    #     SELECT * from welfare_lottery_double ORDER BY code DESC LIMIT 20;
    # """
    sql = """
        SELECT * from welfare_lottery_double ORDER BY code DESC;
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
print(f'total={len(data)}')
blueData = [item['blue'] for item in data]
# welfareLotteryRatioPie(blueData, range(1, 17))
blueLen = len(blueData)
# for i in range(1, 17):
#     count = blueData.count(i)
#     print(f'blue: {i if i >= 10 else "0" + str(i)} count={count} ratio={count / blueLen}')
blueList: List[Dict[str, Union[str, int]]] = [{'lable': i, 'count': blueData.count(i), 'ratio': blueData.count(i) / blueLen} for i in range(1, 17)]
# print(blueList)
blueSortList = sorted(blueList, key=lambda x: x['count'], reverse=True)
for i in blueSortList:
    label = i['lable']
    count = i['count']
    ratio = i['ratio']
    print(f'blue: {label} count={count} ratio={ratio}')
# 只有使用np.array创建的数组才能使用flatten函数进行降维
redData = np.array([item['reds'] for item in data]).reshape(-1).tolist()
# welfareLotteryRatioPie(redData, range(1, 34))
redLen = len(redData)
# for i in range(1, 34):
#     count = redData.count(i)
#     print(f'red: {i if i >= 10 else "0" + str(i)} count={count} ratio={count / redLen}')
redList: List[Dict[str, Union[str, int]]] = [{'lable': i, 'count': redData.count(i), 'ratio': redData.count(i) / redLen} for i in range(1, 34)]
# print(blueList)
redSortList = sorted(redList, key=lambda x: x['count'], reverse=True)
for i in redSortList:
    label = i['lable']
    count = i['count']
    ratio = i['ratio']
    print(f'red: {label} count={count} ratio={ratio}')
# 02 05 13 22 27 32 01
class History:  
    def __init__(self, code: str, date: str, reds: List[int], blue: int, leval: int):  
        self.code = code
        self.date = date
        self.blue = blue
        self.reds = reds
        self.leval = leval

def winHistory(reds: List[int], blue: int):
    levals: List[History] = []
    for item in data:
        iBlue = item['blue']
        iReds: List[int] = item['reds']
        leval = checkLevelHistory(iReds, iBlue, reds, blue)
        if leval != 0:
            levals.append(History(item['code'], item['date'], iReds, iBlue, leval))
    return levals
# levals = winHistory([2,5,13,22,27,32], 1)
# levals = winHistory([4,6,15,17,18,26], 11)
# levals = winHistory([2,7,11,19,20,23], 8)
levals = winHistory([16,20,22,26,30,32], 16)
for item in levals:
    if item.leval < 6:
        print(f'code={item.code} date={item.date} leval={item.leval}')
# 退出
connect.close()
cursor.close()