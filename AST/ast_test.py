from profiler import Profiler
from analytics import Analytics
from profilerast import ProfilerAST
import requests
import re
import json
import time
"""
def B(temp, arr):
    arr.append(temp[:])

def C():
    temp = []
    arr = []
    for x in range(60):
        temp.append(x)
    arr.append(temp[:])

    B(temp, arr)


def main():
    y = 1
    for x in range(y):

        newProfiler = ProfilerAST()
        newProfiler.run(C)
        
"""

def main():
    C()

def C():
    temp = []
    arr = []
    for x in range(10):
        temp.append(x)

    arr.append(temp[:])

    B(temp, arr)

def B(temp, arr):
    arr.append(temp)

