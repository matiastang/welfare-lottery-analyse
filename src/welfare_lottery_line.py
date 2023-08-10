#!/usr/bin/python3
#coding=utf-8

'''
Author: matiastang
Date: 2022-08-12 10:59:35
LastEditors: matiastang
LastEditTime: 2023-07-06 11:09:22
FilePath: /matias-TensorFlow/src/welfareLottery/welfare_lottery_line.py
Description: welfare lottery 折线趋势
'''

import pymysql
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# 显示饼图
def showPie(data: list, range: list):
    # 标签名称
    # labels = list(map(lambda i: str(i) if i >= 10 else ('0' + str(i)), range(1, 17)))
    labels = [(str(v) if v >= 10 else ('0' + str(v))) for v in range]
    # 标签数据
    sizes = [data.count(v) for v in labels]
    print(labels, sizes)
    # ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33']
    # [306, 296, 251, 275, 275, 328, 289, 280, 305, 293, 274, 281, 278, 333, 295, 270, 296, 287, 305, 297, 250, 317, 281, 271, 269, 302, 299, 262, 273, 252, 272, 290, 256]
    # [306, 296, 251, 275, 275, 328, 289, 280, 305, 293, 274, 281, 278, 333, 295, 270, 296, 287, 305, 297, 250, 317, 281, 271, 269, 302, 299, 262, 273, 252, 272, 290, 256]
    # 01,02,06,09,14,17,19,22,26,27
    # 设置
    plt.pie(sizes,pctdistance=0.85, labels=labels, radius=1, 
            autopct='%1.3f%%', shadow=False, startangle=90,wedgeprops=dict(width=0.3, edgecolor='w'))
    # 显示
    plt.show()

# 显示折线图
def showLine(data: list):
    # print(xValues)
    # 解决中文显示问题
    # 查看路径
    print(matplotlib.matplotlib_fname())
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 绘图
    plt.figure(figsize=(15,6))# 画布
    # plt.rcParams['font.family']='MicroSoft YaHei'  #设置字体，默认字体显示不了中文
    plt.plot(np.linspace(1, len(data), len(data)), data)
    # plt.plot(xValues, values)
    # plt.plot([k for k, v in values], values)
    plt.title("blue 则线图")# 设置图表标题
    plt.xlabel('code')# x轴标题
    plt.ylabel('blue')# y轴标题
    plt.ylim(1, 16)
    # plt.xticks([])
    # plt.xticks(np.linspace(0, len(xValues) - 1, len(xValues)), xValues, rotation ='vertical')
    # plt.yticks([])
    plt.show()# 显示

# 显示red折线图list[list[str]]
def showRedLine(data: list):
    # 画布
    plt.figure(figsize=(15,6))
    plt_label = 0
    for values in data:
        plt_label += 1
        plt.plot(np.linspace(1, len(values), len(values)), [int(i) for i in values], label = '第'+ str(plt_label) + '条线段')
    # plt.rcParams['font.family']='MicroSoft YaHei'  #设置字体，默认字体显示不了中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 设置图表标题
    plt.title("red line")
    # x轴标题
    plt.xlabel('code')
    # y轴标题
    plt.ylabel('red')
    # y轴范围
    plt.ylim(1, 33)
    # 显示
    plt.show()


# 链接mysql
connect = pymysql.connect(
    # host='127.0.0.1',
    host='110.41.145.30',
    db="mt_scrapy",
    # user="root",
    user='matiastang',
    passwd="MySQL_18380449615",
    charset='utf8',
    use_unicode=True,
    cursorclass=pymysql.cursors.DictCursor
)
# 通过cursor执行增删查改
cursor = connect.cursor()

# 查询
# sql = """
#     SELECT code, blue from welfare_lottery_ssq
# """

# sql = """
#     SELECT code, date, red, blue from welfare_lottery_ssq as tab where tab.code like '2021%'
# """
# sql = """
#     SELECT * from welfare_lottery_ssq
# """
sql = """
    SELECT * from welfare_lottery_double
"""

codes = []
dates = []
reds = []
blues = []

try:
    cursor.execute(sql)
    #这是获取表中第一个数据
    # result = cursor.fetchone()
    #这是查询表中所有的数据
    result=cursor.fetchall()
    # code数据
    codes = [item['code'] for item in result]
    # date数据
    dates = [item['date'] for item in result]
    # red数据
    reds = [item['red'] for item in result]
    # blue数据
    blues = [item['blue'] for item in result]
    
    
except:
    print('查询失败----')
    connect.rollback()

# 显示
# showLine(blues[:20])
# showPie(blues, range(1, 17))
# red数据降维
allReds = np.array([v.split(',') for v in reds]).ravel()
# showRedLine([v.split(',') for v in reds])
redData = [v.split(',') for v in reds]
redDatas = [list(map(lambda item: item[v], redData)) for v in range(0, 5)]
# showRedLine(redDatas)
# ndarray转list
allReds = allReds.tolist()
showPie(allReds, range(1, 34))

# 退出
connect.close()
cursor.close()