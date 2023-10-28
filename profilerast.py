import ast
import time

class ProfilerAST:
    def __init__(self):
        self.function_timings = {}
        self.total_time = 0

    def profile(self, func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            execution = (end - start) * 1000
            if func.__name__ not in self.function_timings:
                self.function_timings[func.__name__] = execution
            else:
                self.function_timings[func.__name__] += execution

            self.total_time += execution
            return result

        return wrapper

    def run(self, code, func_name, *args, **kwargs):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                function_name = node.name
                decorated = self.profile(node)
                locals()[function_name] = decorated
                exec(compile(ast.Module([node], []), '<string>', 'exec'))
                function_to_run = locals()[function_name]
                function_to_run(*args, **kwargs)
                self.printFunctionTimings()

    def printFunctionTimings(self):
        sorted_items = sorted(self.function_timings.items(), key=lambda x: x[1], reverse=True)
        for key, value in sorted_items:
            print(f"Function {key} has time {value} ms")
        print(f"Total time: {self.total_time} ms")
