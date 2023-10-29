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

		total_time += execution
		return result
	return wrapper

def walker(node):
	print("************")
	for n in ast.walk(node):
		pass



if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 profilerast1.py <path/to/code_file.py> <function_name>")
	else:
		file_path = sys.argv[1]
		function_name = sys.argv[2]

		try:
			ast1 = get_ast(file_path)
			function_node = get_function(ast1, function_name)
			
			for node in ast.walk(function_node):

				print(ast.dump(node, indent=4))
				print("---")
		except Exception as e:
			print(f"An error occurred: {e}")