import ast
import sys
import time

function_timings = {}
total_time = 0

def get_ast(file_path):
	with open(file_path, "r") as source_code:
		tree = ast.parse(source_code.read())
	return tree

def get_function(tree, function_name):
	for node in ast.walk(tree):
		if isinstance(node, ast.FunctionDef) and node.name == function_name:
			return node
	return None

def profile(func):
	def wrapper(*args, **kwargs):
		global function_timings, total_time
		start = time.perf_counter()
		result = func(*args, **kwargs)
		end = time.perf_counter()

		execution = (end-start) * 1000
		if func.__name__ not in function_timings:
			function_timings[func.__name__] = execution
		else:
			function_timings[func.__name__] += execution