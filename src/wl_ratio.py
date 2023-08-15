#!/usr/bin/python3
#coding=utf-8

'''
Author: matiastang
Date: 2023-07-06 11:14:59
LastEditors: matiastang
LastEditTime: 2023-08-15 14:08:01
FilePath: /welfare-lottery-analyse/src/wl_ratio.py
Description: 比例
'''

from typing import List, Dict, Union
import pymysql
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from utils.transform import transformReds
from utils.check import checkLevelHistory
import logging
import math
logging.basicConfig(level=logging.ERROR)

print(mpl.__version__)

mpl.rcParams['font.family'] = ['Hiragino Sans']
  
# n = 16  
# k = 1 
# combinations = math.comb(n, k)
# probability = combinations / (n**k)
redN = 33
redK = 6
redCombinations = math.comb(redN, redK)
 
blueN = 16
blueK = 1
blueCombinations = math.comb(blueN, blueK)

combinations = redCombinations * blueCombinations
print(f'combinations={combinations}')

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
# 获取历史
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
print(f'already combinations={len(data)}')
# 蓝球比例
blueData = [item['blue'] for item in data]
# 饼图
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
# 红球比例
# 只有使用np.array创建的数组才能使用flatten函数进行降维
redData = np.array([item['reds'] for item in data]).reshape(-1).tolist()
# 饼图
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
        
    def __hash__(self):  
        return hash((self.blue, tuple(self.reds)))
        
    def __eq__(self, other):  
        if isinstance(other, History):
            if self.blue != other.blue:
                return False 
            sReds = self.reds
            oReds = other.reds
            return set(sReds) == set(oReds)
        return False  
# 查询历史中奖等级
def winHistory(historys: List[Dict[str, Union[str, int, List[int]]]], reds: List[int], blue: int):
    levals: List[History] = []
    for item in historys:
        iBlue = item['blue']
        iReds: List[int] = item['reds']
        leval = checkLevelHistory(iReds, iBlue, reds, blue)
        if leval != 0:
            levals.append(History(item['code'], item['date'], iReds, iBlue, leval))
    return levals
# levals = winHistory(data, [2,5,13,22,27,32], 1)
# levals = winHistory([4,6,15,17,18,26], 11)
# levals = winHistory([2,7,11,19,20,23], 8)
# levals = winHistory([16,20,22,26,30,32], 16)
# levals = winHistory([3,12,24,25,32,33], 13)
# levals = winHistory(data, [14,6,22,1,9,19], 1)
# levals = winHistory(data, [4,9,19,31,29,18], 11)
# levals = winHistory(data, [10,21,24,25,27,32], 7)
levals = winHistory(data, [12,16,26,31,32,33], 6)
for item in levals:
    if item.leval < 6:
        print(f'code={item.code} date={item.date} leval={item.leval}')
arr = [item.leval for item in levals if item.leval < 6]
print(f'leval total {len(arr)}')
# 查询历史重复
def repetitionHistory():
    historys: List[History] = []
    for item in data:
        # if item['code'] == '2023092':
        #     historys.append(History(item['code'], item['date'], item['reds'], item['blue'], 0))
        historys.append(History(item['code'], item['date'], item['reds'], item['blue'], 0))
    return [item for item, count in Counter(historys).items() if count > 1]
repetitionList = repetitionHistory()
if len(repetitionList) > 0:
    print('历史重复：', len(repetitionList))
    for item in repetitionList:
        print(f'code={item.code} date={item.date} blue={item.blue} reds={item.reds} leval=1')
else:
    print('历史无重复')
# 前历史次数及最高
levalMin = 100
levalMax = 0
def repetitionLevalHistory():
    global levalMin
    global levalMax
    # historys: List[History] = []
    nums: List[int] = []
    for i, item in enumerate(data[:100]):
    # for i, item in enumerate(data):
        code = item['code']
        date = item['date']
        reds = item['reds']
        blue = item['blue']
        # historys.append(History(code, date, reds, blue, 0))
        levals = winHistory(data[i + 1:], reds, blue)
        arr = [item.leval for item in levals if item.leval < 6]
        num = len(arr)
        nums.append(num)
        if (num > levalMax):
            levalMax = num
        if (num < levalMin):
            levalMin = num
        # print(f'code={code} date={date} reds={reds} blue={blue} levals={arr}')
        # print(f'code={code} leval len={len(levals)} leval < 6 len={len(arr)} levals={arr}')
    return nums
counts= repetitionLevalHistory()
counts.sort()
# print(f'nums={counts}')
print(f'min={levalMin}-{levalMax}=max')
index = int(len(counts) / 2)
print(f'中位数={counts[index]}')
avg = sum(counts)/len(counts)
print(f'平均数={avg}')
# 连续
def continuousHistory():
    continuous: List[Dict[str, Union[str, int]]] = []
    maxIndex = len(data) - 1
    continuousBlue = 0
    continuousCount = 0
    for i, item in enumerate(data[::-1]):
        blue = item['blue']
        if (continuousBlue != 0 and (continuousBlue != blue or i == maxIndex)):
            if (continuousCount <= 1):
                continuousBlue = blue
                continuousCount = 1
                continue
            continuous.append({ 'code': item['code'], 'blue': continuousBlue, 'count': continuousCount })
            continuousBlue = blue
            continuousCount = 1
        else:
            if (continuousBlue == 0):
                continuousBlue = blue
            continuousCount += 1
    return continuous
continuous = continuousHistory()
print(f'continuous len={len(continuous)}')
for item in continuous:
    code = item['code']
    blue = item['blue']
    count = item['count']
    print(f'code={code} blue={blue} count={count}')
    # if blue == 7:
    #     print(f'code={code} blue={blue} count={count}')
# 相似度
def similarityHistory():
    # similarity: List[Dict[str, int]] = []
    similarity: List[int] = []
    previousBlue = 0
    for i, item in enumerate(data[::-1]):
        blue = item['blue']
        if previousBlue == 0:
            previousBlue = blue
            # similarity.append({ 'code': item['code'], 'value': 16 })
            similarity.append(16)
        else:
            # similarity.append({ 'code': item['code'], 'value': abs(previousBlue - blue) })
            similarity.append(abs(previousBlue - blue))
            previousBlue = blue
    return similarity
similaritys = similarityHistory()
similarityLen = len(similaritys)
similarityList: List[Dict[str, Union[str, int]]] = [{'lable': i, 'count': similaritys.count(i), 'ratio': similaritys.count(i) / similarityLen} for i in range(0, 17)]
similaritySortList = sorted(similarityList, key=lambda x: x['count'], reverse=True)
for i in similaritySortList:
    label = i['lable']
    count = i['count']
    ratio = i['ratio']
    print(f'similarity: {label} count={count} ratio={ratio}')
# next probability
def nextProbabilityHistory(last: int):
    probability: List[int] = []
    previousIsLast = False
    for i, item in enumerate(data[::-1]):
        blue = item['blue']
        if blue == last:
            if (previousIsLast):
                probability.append(blue)
            previousIsLast = True
            
        else:
            probability.append(blue)
            previousIsLast = False
    return probability
# probabilitys = nextProbabilityHistory(7)
probabilitys = nextProbabilityHistory(6)
probabilityLen = len(probabilitys)
probabilityList: List[Dict[str, Union[str, int]]] = [{'lable': i, 'count': probabilitys.count(i), 'ratio': probabilitys.count(i) / probabilityLen} for i in range(1, 17)]
probabilitySortList = sorted(probabilityList, key=lambda x: x['count'], reverse=True)
for i in probabilitySortList:
    label = i['lable']
    count = i['count']
    ratio = i['ratio']
    print(f'probability: {label} count={count} ratio={ratio}')
# 退出
connect.close()
cursor.close()