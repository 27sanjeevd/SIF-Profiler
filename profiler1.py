import sys
import time
import traceback
import linecache

class Profiler:

	def __init__(self, test_timing=False, test_memory=False, test_lines=False, 
		timing_isolation=False):

		self.function_timings = {}
		"""
		The stack has arrays of 4 elements
		stack[0] = Function name
		stack[1] = time of execution
		stack[2] = total_extra time from other function (to be subtracted at end)
		stack[3] = current pause of execution time
		"""
		self.function_stack = []
		self.function_overhead_stack = [0]

		self.line_traces = []
		self.line_prev_time = 0
		self.prev_line_num = -1

		self.function_memory_usage = {}

		self.function_call_counter = 0
		self.global_position = -1

		self.calibration_times = []

		self.memory_frame = 0

		self.test_timing = test_timing
		self.test_memory = test_memory
		self.test_lines = test_lines

		"""
		Used identify if we want to add function sub-function timings to current function 
		times, or if we want to isolate the function time

		"""
		self.timing_isolation = timing_isolation


	def run(self, func_name, *args):
		try:
			sys.settrace(self.trace_calls)
			func_name(*args)
		except Exception as e:
			traceback.print_exc()
			print(f"An error has occurred {e}")

		sys.settrace(None)


	def trace_calls(self, frame, event, arg):
		beg = time.perf_counter()
		if self.test_timing == True:
			self.timing_trace_function(frame, event, arg, beg)

		
		if event != "call" and event != "return":
			end = time.perf_counter()
			self.function_overhead_stack[-1] += (end - beg) * 1000


		return self.trace_calls


	def timing_trace_function(self, frame, event, arg, s_time):
		if self.test_lines == True:
			function_name = frame.f_code.co_name
			line_num = frame.f_lineno
			if self.prev_line_num != line_num:
				self.prev_line_num = line_num

				curr_time = time.perf_counter()
				time_diff = curr_time - self.line_prev_time
				self.line_prev_time = curr_time


				if event == "call":
					self.global_position += 1

				self.line_traces.append([function_name, time_diff, line_num, self.global_position, 
					linecache.getline(frame.f_code.co_filename, line_num).strip()])
				
				if event == "return":
					self.global_position -= 1


		if event == "call":
			self.function_call_counter += 1

			function_name = frame.f_code.co_name
			timestamp = time.perf_counter()

			if len(self.function_stack) != 0:
				self.function_stack[-1][3] = timestamp

			self.function_overhead_stack[-1] += (timestamp - s_time) * 1000

			self.function_stack.append([function_name, timestamp, 0, 0])
			self.function_overhead_stack.append(0)

		elif event == "return":
			prev = self.function_stack[-1]
			curr_time = time.perf_counter();

			"""
			total time in milliseconds
			need to figure out a way to subtract the overhead from all the previous
			lines up until this point
			"""
			if self.timing_isolation:
				total_time = -1 * prev[1] * 1000 - prev[2]
			else:
				#total_time = (curr_time - prev[1]) * 1000
				total_time = -1 * prev[1] * 1000
			total_time -= self.function_overhead_stack[-1]

			if len(self.function_overhead_stack) > 1:
				self.function_overhead_stack[-2] += self.function_overhead_stack[-1]
				self.function_overhead_stack.pop(-1)

			if self.function_stack[-1][0] not in self.function_timings:
				self.function_timings[self.function_stack[-1][0]] = total_time + time.perf_counter() * 1000
			else:
				self.function_timings[self.function_stack[-1][0]] += total_time + time.perf_counter() * 1000

			self.function_stack.pop(-1)
			if len(self.function_stack) != 0:
				self.function_stack[-1][2] += (time.perf_counter() - self.function_stack[-1][3]) * 1000
				self.function_stack[-1][3] = 0


	def printFunctionTimings(self):
		sorted_dict = dict(sorted(self.function_timings.items(), key=lambda item: -item[1]))

		amt = None
		for key, value in sorted_dict.items():
			if amt == None:
				amt = value
			#print(f"Function {key} with time {value}")

		return amt


	def printLineTraces(self):
		for x in self.line_traces:
			temp = "-" * (2 * x[3])
			print(f"Function {x[0]} ran line {x[2]} in time {x[1]}: {x[4]}")

	def clear(self):
		self.function_timings = {}

		self.function_stack = []
		self.function_overhead_stack = [0]

		self.line_traces = []
		self.line_prev_time = 0
		self.prev_line_num = -1

		self.function_memory_usage = {}

		self.function_call_counter = 0
		self.global_position = -1

		self.calibration_times = []

		self.memory_frame = 0






























