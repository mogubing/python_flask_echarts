#coding:utf-8
"""
@author:ghh
@file:yield.py
@time:2017/12/6 9:50
"""
def fab(max):
    n,a,b=0,0,1
    while n<max:
        yield b
        a,b=b,a+b
        n=n+1
for i in fab(9):
    print i
# 小记：每次调用都有返回值，保持了函数的可用性；且内存空间占用小。