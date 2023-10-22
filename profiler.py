import sys
import time
import traceback
import linecache

class Profiler:
	def __init__(self, test_timing=False, timing_isolation=False, timed_functions=None):
		self.function_timings = {}
		self.function_stack = []
		self.function_runtime_overhead = [0]


		self.test_timing = test_timing
		self.timing_isolation = timing_isolation

		self.timing_functions = []
		if timed_functions is not None:
			self.timing_functions = timed_functions
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
		

		#end = time.perf_counter()
		#self.function_runtime_overhead[-1] += (end - beg) * 2000 + self.calibration_count
		

		return self.trace_calls

	def function_timing(self, frame, event, arg, s_time):
		if event == "call":
			self.function_call_timing(frame)

		elif event == "return":
			self.function_return_timing()
		
		#adds the overhead of calling "function_timing" to the overhead
		self.function_runtime_overhead[-1] += (time.perf_counter() - s_time) * \
			1950 + self.calibration_count

	def function_call_timing(self, frame):
		func_name = frame.f_code.co_name

		#if we're timing isolation, then add the time of when current function gets paused 
		#to the function stack
		if self.timing_isolation and len(self.function_stack) > 0:
			self.function_stack[-1][2] = time.perf_counter()

		#add the new function information to the function_stack
		self.function_stack.append([func_name, time.perf_counter(), 0, 0])
		#add the current runtime to the overhead stack
		self.function_runtime_overhead.append(0)

	def function_return_timing(self):
		prev = self.function_stack[-1]
		temp = self.function_runtime_overhead[-1]

		#if timing isolation and there was a function before it
		if not self.timing_isolation and len(self.function_runtime_overhead) > 1:
			#adds the current_overhead to the parent timing overhead
			self.function_runtime_overhead[-2] += self.function_runtime_overhead[-1]
			self.function_runtime_overhead.pop(-1)

		timestamp = time.perf_counter()
		total_time = (timestamp - prev[1]) * 1000 - temp

		#adds the current funtime runtime info to the dictionary of values
		if self.timing_functions == [] or self.function_stack[-1][0] in self.timing_functions:
			if self.function_stack[-1][0] not in self.function_timings:
				self.function_timings[self.function_stack[-1][0]] = total_time
			else:
				self.function_timings[self.function_stack[-1][0]] += total_time

		#removes it from the current stack
		self.function_stack.pop(-1)

	def printFunctionTimings(self):
		for key, value in self.function_timings.items():
			print(f"Function {key} has time {value}")





