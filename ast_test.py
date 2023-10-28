from profiler import Profiler
from analytics import Analytics
from profilerast import ProfilerAST
import requests
import re
import json
import time

def looper():
    for _ in range(150):
        A()

def A():
    for _ in range(120):
        C()
        B()

def B():
    global temp, arr
    arr.append(temp[:])

def C():
    temp = []
    arr = []
    for x in range(60):
        temp.append(x)
    arr.append(temp[:])

def getReport():
    with open('reports.txt', 'r') as file:
        for line in file:
            contents = line
            link1 = 'https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/' + str(contents)
            response = requests.get(link1[:-1])
            parseReport(response.text)


def parseReport(report):
    dict1 = json.loads(report)

    first_name = dict1[0]['first_name']
    last_name = dict1[0]['last_name']
    date = dict1[0]['filing_date']
    #print(first_name, last_name, date)

    transactions = dict1[0]['transactions']
    for x in range(len(transactions)):
        #print(transactions[x])
        pass



def main():
    y = 1
    for x in range(y):

        newProfiler = ProfilerAST()
        newProfiler.run(C)
        

if __name__ == "__main__":
    main()
