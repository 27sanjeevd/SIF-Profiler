from profiler import Profiler
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

temp = []
arr = []
for x in range(50):
    temp.append(x)

def main():
    y = 1
    for x in range(y):

        newProfiler = Profiler(test_timing=True)
        temp = []

        start1 = time.perf_counter()
        newProfiler.run(looper)
        end1 = time.perf_counter()
        end_profile = newProfiler.printFunctionTimings()

        #newProfiler.clear()

        start = time.perf_counter()
        looper()
        end = time.perf_counter()

        
        print((end1-start1)*1000, " original")
        print((end1-start1)*1000 - newProfiler.function_runtime_overhead[-1], " original - overhead")
        print((end-start)*1000, " default")
        

if __name__ == "__main__":
    main()
