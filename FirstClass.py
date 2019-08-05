# -*- coding: utf-8 -*-
"""
Created on 2019/6/25 11:08
@Author  : zhangh
@File    : FirstClass.py
@Project : PythonDemo
"""
class FirstClass:
    def setdata(self, value):
        self.data = value
    def display(self):
        print(self.data)

class SecondClass(FirstClass):
    def display(self):
        print("Current value = %s" % self.data)

class ThirdClass(SecondClass):
    def __init__(self, value):
        self.data = value
    def __add__(self, other):
        return ThirdClass(self.data + other)
    def __str__(self):
        return  '[ThirdClass: %s]' % self.data
    def mul(self, other):
        self.data *= other

class Person:
    def __init__(self, name, job):
        self.name = name
        self.job = job
    def info(self):
        return (self.name, self.job)

