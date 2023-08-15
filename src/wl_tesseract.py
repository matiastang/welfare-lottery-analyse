#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: matiastang
Date: 2023-08-15 11:24:56
LastEditors: matiastang
LastEditTime: 2023-08-15 14:04:53
FilePath: /welfare-lottery-analyse/src/wl_tesseract.py
Description: wl_tesseract
'''

import pytesseract
from PIL import Image
# file = r"/Users/matias/matias/matiasResources/images/jpg/2023088.jpg"
file = r"/Users/matias/matias/matiasResources/images/jpg/2023088-code.jpg"

# 建议图像识别前，先对图像进行灰度化和 二值化，以提高文本识别率
# image = Image.open(file)
# Img = image.convert('L')   # 灰度化
# #自定义灰度界限，这里可以大于这个值为黑色，小于这个值为白色。threshold可根据实际情况进行调整(最大可为255)。
# threshold = 180
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# photo = Img.point(table, '1')  #图片二值化
# #保存处理好的图片
# photo.save(newfile)

image = Image.open(file)
# 解析图片，lang='chi_sim'表示识别简体中文，默认为English
# 如果是只识别数字，可再加上参数config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
# content = pytesseract.image_to_string(image, lang='chi_sim')
content = pytesseract.image_to_string(image, lang='eng+chi_sim')
# content = pytesseract.image_to_string(image, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=A.0123456789')
print(content)