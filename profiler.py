import sys
import time
import traceback
import linecache

class Profiler:

	def __init__(self, test_timing=False):
		self.function_timings = {}
		self.function_stack = []
		self.function_runtime_overhead = [0]


		self.test_timing = test_timing

		beg = time.perf_counter()

		for _ in range(5000):
		    self.test_func()
		end = time.perf_counter()

		self.calibration_count = (end - beg)/5000

	def test_func(self):
		pass

	def run(self, func_name, *args):
	    try:
	        sys.setprofile(self.trace_calls)
	        func_name(*args)
	    except Exception as e:
	        traceback.print_exc()
	        print(f"An error has occurred {e}")
	    finally:
	        sys.setprofile(None)

	def trace_calls(self, frame, event, arg):
		
		
		beg = time.perf_counter()

		
		if self.test_timing:
			self.function_timing(frame, event, arg, beg)
		

		end = time.perf_counter()
		self.function_runtime_overhead[-1] += (end - beg) * 2000 + self.calibration_count
		

		return self.trace_calls

	def function_timing(self, frame, event, arg, s_time):
		if event == "call":
			func_name = frame.f_code.co_name
			timestamp = time.perf_counter()

			self.function_stack.append([func_name, timestamp])
			self.function_runtime_overhead.append(0)
		elif event == "return":
			prev = self.function_stack[-1]
			temp = self.function_runtime_overhead[-1]

			if len(self.function_runtime_overhead) > 1:
				self.function_runtime_overhead[-2] += self.function_runtime_overhead[-1]
				self.function_runtime_overhead.pop(-1)

			timestamp = time.perf_counter()
			total_time = (timestamp - prev[1]) * 1000 - temp

			if self.function_stack[-1][0] not in self.function_timings:
				self.function_timings[self.function_stack[-1][0]] = total_time
			else:
				self.function_timings[self.function_stack[-1][0]] += total_time

			self.function_stack.pop(-1)

	def printFunctionTimings(self):
		for key, value in self.function_timings.items():
			print(f"Function {key} has time {value}")






