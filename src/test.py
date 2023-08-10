#!/usr/bin/python3
#coding=utf-8
'''
Author: matiastang
Date: 2023-07-11 17:44:51
LastEditors: matiastang
LastEditTime: 2023-07-11 17:51:33
FilePath: /matias-TensorFlow/src/test.py
Description: 测试
'''
from typing import List

def splitReds(reds: str) -> List[int]:
    redList = reds.split(',')
    return list([int(item) for item in redList])

redList = splitReds('01,02,03,04,05')
print(redList)

'''
List[int]
链接：https://www.zhihu.com/question/543133712/answer/2574729076

它是所谓的“类型提示”（或“函数注释”；这些从 Python 3.0开始可用）。-> List[int]意味着函数应该返回一个整数列表。nums: List[int], target: int意味着应该nums是一个整数列表，并且应该target是一个整数。不过，这不是硬性要求，即您仍然可以使用为这些参数传递的不同类型的对象调用该函数，并且该函数也可以返回与整数列表不同的东西（不像在 Java 等其他语言中提供错误类型会导致编译错误）。换句话说：类型提示与程序执行无关，它们在运行时被忽略（忽略类型提示只是默认行为，但它们在运行时通过 可用__annotations__，所以你可以用它们做点什么）。类型提示可以表达作者的意图，并且可以在程序执行之前通过mypy 之类的工具进行检查（例如，这些可以检查一个函数是否仅使用正确类型的参数调用并返回正确类型的内容）。请注意，List在标准命名空间中不可用（与 不同list），但（至少在 Python 3.9 之前）需要从typing其中导入为标准类型提供其他类型，如Set, Dict,Tuple等Callable。允许定义自己的类型提供其他类型的类型化版本，例如NamedTuple代替namedtuple从 Python 3.9 开始，也可以使用标准list构造函数来获取类型提示。
'''