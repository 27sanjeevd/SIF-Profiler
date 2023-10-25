import sys
import time
import json
import psutil
import traceback
import linecache

class Profiler:
	def __init__(self, test_timing=True, test_lines=False, timing_isolation=False, \
		timing_functions=None, test_memory=False):
		self.function_timings = {}
		self.function_stack = []
		self.function_runtime_overhead = [0]
		self.total_time = 0

		self.memory_usage_track = {}
		self.memory_prev_time = -1
		self.memory_prev_no = -1

		self.line_timings_track = {}
		self.line_timings_overall = {}
		self.line_prev_time = -1
		self.line_prev_no = -1
		self.line_counter = 0

		self.test_lines = test_lines
		self.test_timing = test_timing
		self.test_memory = test_memory
		self.timing_isolation = timing_isolation

		self.timing_functions = []
		if timing_functions is not None:
			self.timing_functions = timing_functions

		beg = time.perf_counter()
		for _ in range(5000):
		    self.test_func()
		end = time.perf_counter()

		self.calibration_count = (end - beg)/5000


		self.profile_head_function = ""
		

	#test function used to test how long the function call of the tracing function takes
	def test_func(self):
		pass



	def run(self, func_name, *args):
	    try:
	    	self.clear()
	    	self.profile_head_function = func_name.__name__
	    	sys.settrace(self.trace_calls)
	    	func_name(*args)
	    except Exception as e:
	    	traceback.print_exc()
	    	print(f"An error has occurred {e}")
	    finally:
	    	sys.settrace(None)
	    	self.dumpFileTrace()



	def trace_calls(self, frame, event, arg):
		
		beg = time.perf_counter()
		
		#calls the timing function
		if self.test_timing:
			curr_time = time.perf_counter()
			self.function_timing(frame, event, arg, curr_time)

			#line timing test function
			if self.test_lines:
				self.line_timing(frame, event, arg, beg)
		
		
		#stores new line information in the variables
		if self.timing_functions == [] or frame.f_code.co_name in self.timing_functions:
			self.line_prev_no = frame.f_lineno
			self.line_prev_time = time.perf_counter()
		

		#adds the overhead of calling "function_timing" to the overhead
		self.function_runtime_overhead[-1] += (time.perf_counter() - beg) * \
			2000 + self.calibration_count * 2000
		
		return self.trace_calls



	def line_timing(self, frame, event, arg, beg):
		if self.line_prev_time != -1 and \
			(self.timing_functions == [] or frame.f_code.co_name in self.timing_functions):
		
			#gets the runtime of the previous line
			runtime = (beg - self.line_prev_time) * 1000

			#stores that previous line's runtime in the dictionary
			if self.line_prev_no not in self.line_timings_track:

				#line_timings_track counts the individual runtimes every time the line is called
				self.line_timings_track[self.line_prev_no] = [(self.line_counter, runtime)]
				#line_timings_overall counts the overall runtime of each specific line
				self.line_timings_overall[self.line_prev_no] = runtime

			else:
				self.line_timings_track[self.line_prev_no].append((self.line_counter, runtime))
				self.line_timings_overall[self.line_prev_no] += runtime
			#updates the line counter to track what order the lines have been called in
			self.line_counter += 1




	def function_timing(self, frame, event, arg, curr_time):
		if event == "call":
			self.function_call_timing(frame, curr_time)

		elif event == "return":
			self.function_return_timing(curr_time)
		


	def function_call_timing(self, frame, curr_time):
		#time diff as we don't start the tracker immediately at the beginning of profiler
		diff_time = time.perf_counter() - curr_time
		func_name = frame.f_code.co_name

		#if we're timing isolation, then add the time of when current function gets paused 
		#to the function stack
		if self.timing_isolation and len(self.function_stack) > 0:
			self.function_stack[-1][2] = time.perf_counter() - diff_time

		#add the new function information to the function_stack
		self.function_stack.append([func_name, time.perf_counter() - diff_time, 0, 0])
		#add the current runtime to the overhead stack
		self.function_runtime_overhead.append(0)



	def function_return_timing(self, curr_time):
		prev = self.function_stack[-1]
		temp = self.function_runtime_overhead[-1]

		diff_time = time.perf_counter() - curr_time

		#if timing isolation and there was a function before it
		if not self.timing_isolation and len(self.function_runtime_overhead) > 1:
			#adds the current_overhead to the parent timing overhead
			self.function_runtime_overhead[-2] += self.function_runtime_overhead[-1]
			self.function_runtime_overhead.pop(-1)

		timestamp = time.perf_counter() - diff_time
		total_time = (timestamp - prev[1]) * 2000 - temp

		#adds the current funtime runtime info to the dictionary of values
		if self.timing_functions == [] or self.function_stack[-1][0] in self.timing_functions:
			if self.function_stack[-1][0] not in self.function_timings:
				self.function_timings[self.function_stack[-1][0]] = total_time
			else:
				self.function_timings[self.function_stack[-1][0]] += total_time

			self.total_time += total_time

		#removes it from the current stack
		self.function_stack.pop(-1)



	def printFunctionTimings(self):
		sorted_items = sorted(self.function_timings.items(), key=lambda x: x[1], reverse=True)
		for key, value in sorted_items:
			print(f"Function {key} has time {value}")
		print("----------------")


	def printLineTimings(self):
		sorted_items = sorted(self.line_timings_overall.items(), key=lambda x: x[1], reverse=True)
		for key, value in sorted_items:
			print(f"Line {key} has time {value}")
		print("----------------")



	def dumpFileTrace(self):
		with open(f'{self.profile_head_function}.json', 'w') as file:
			json.dump(self.line_timings_track, file)

	def clear(self):
		self.function_timings = {}
		self.function_stack = []
		self.function_runtime_overhead = [0]
		self.total_time = 0

		self.memory_usage_track = {}
		self.memory_prev_time = -1
		self.memory_prev_no = -1

		self.line_timings_track = {}
		self.line_timings_overall = {}
		self.line_prev_time = -1
		self.line_prev_no = -1
		self.line_counter = 0

		self.profile_head_function = ""



