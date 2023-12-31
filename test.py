from profiler import Profiler
from analytics import Analytics
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
    global temp, arr
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


temp = []
arr = []
for x in range(60):
    temp.append(x)

def main():
    y = 1
    for x in range(y):

        newProfiler = Profiler()

        newProfiler.test_timing = True
        newProfiler.test_memory = True
        newProfiler.test_lines = True
        newProfiler.timing_isolation = True
        newProfiler.timing_functions = ['getReport', 'parseReport']

        temp = []

        start1 = time.perf_counter()
        newProfiler.run(getReport)
        end1 = time.perf_counter()

        newProfiler.printFunctionTimings()
        newProfiler.printLineTimings()
        newProfiler.printLineMemory()

        
        analysis = Analytics()
        analysis.load("getReport")

        analysis.view(3)
        

if __name__ == "__main__":
    main()
