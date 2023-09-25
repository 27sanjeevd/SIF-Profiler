from profiler import Profiler
import time

def looper():
	for _ in range(2):
		A()
		C()

def A():
	B()

def B():
	global temp, arr
	arr.append(temp[:])

def C():
	global temp, arr
	arr.append(temp[:])

temp = []
arr = []
for x in range(1000000):
	temp.append(x)

def main():
	newProfiler = Profiler(test_timing=True, timing_isolation=False, test_lines=True)

	start1 = time.time()
	newProfiler.run(looper)
	end1 = time.time()
	end_profile = newProfiler.printFunctionTimings()
	newProfiler.printLineTraces()

	start = time.time()
	looper()
	end = time.time()
	"""
	1) Profiled execution time
	2) Regular execution time
	3) Difference between profiled display time and regular time (measuring error)
	"""
	print((end1 - start1) * 1000)
	print((end - start) * 1000)
	print(end_profile)




if __name__ == "__main__":
	main()