import sys
import time
import json
import psutil
import traceback
import linecache
import matplotlib.pyplot as plt

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
		pass

	def plotMemoryOverall(self):
		pass

	def plotLineTrack(self):
		pass

	def plotLineOverall(self):
		pass