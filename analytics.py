import sys
import time
import json
import psutil
import traceback
import linecache
import matplotlib.pyplot as plt
import numpy as np

class Analytics:
	def __init__(self):
		self.function_timings = {}
		self.memory_usage_track = {}
		self.memory_usage_overall = {}
		self.line_timings_track = {}
		self.line_timings_overall = {}

	def load(self, fileName):
		with open(f"{fileName}.json", "r") as file:
			loaded_dicts = json.load(file)

		self.line_timings_track, self.line_timings_overall, self.function_timings, \
			self.memory_usage_track, self.memory_usage_overall = loaded_dicts


	def view(self, option):
		if option == 0:
			self.plotFunctionTimings()
		elif option == 1:
			self.plotMemoryTrack()
		elif option == 2:
			self.plotMemoryOverall()
		elif option == 3:
			self.plotLineTrack()
		elif option == 4:
			self.plotLineOverall()



	def plotFunctionTimings(self):
		pass



	def plotMemoryTrack(self):
		data = self.memory_usage_track

		global_counters = sorted(set(counter for line_data in data.values() for counter, _ in line_data))

		# Initialize memory data for each line
		memory_data = {line_name: np.zeros(len(global_counters)) for line_name in data.keys()}

		# Fill memory data from the dictionary
		for line_name, line_data in data.items():
		    for global_counter, memory_amount in line_data:
		        memory_data[line_name][global_counters.index(global_counter)] = memory_amount

		# Plotting
		fig, ax = plt.subplots(figsize=(8, 6))

		# Plotting columns for each line
		for line_name, memory_values in memory_data.items():
		    ax.plot(global_counters, memory_values, marker='o', markersize=5, label=line_name)

		ax.set_xlabel('Global Counter')
		ax.set_ylabel('Memory Usage')
		ax.set_title('Memory Usage by Global Counter')
		ax.legend()

		plt.show()



	def plotMemoryOverall(self):
		pass



	def plotLineTrack(self):
		data = self.line_timings_track

		global_counters = sorted(set(counter for line_data in data.values() for counter, _ in line_data))

		# Initialize memory data for each line
		memory_data = {line_name: np.zeros(len(global_counters)) for line_name in data.keys()}

		# Fill memory data from the dictionary
		for line_name, line_data in data.items():
		    for global_counter, memory_amount in line_data:
		        memory_data[line_name][global_counters.index(global_counter)] = memory_amount

		# Plotting
		fig, ax = plt.subplots(figsize=(8, 6))

		# Plotting columns for each line
		for line_name, memory_values in memory_data.items():
		    ax.plot(global_counters, memory_values, marker='o', markersize=2, label=line_name)

		ax.set_xlabel('Global Counter')
		ax.set_ylabel('Memory Usage')
		ax.set_title('Memory Usage by Global Counter')
		ax.legend()

		plt.yscale('log')

		plt.show()



	def plotLineOverall(self):
		pass