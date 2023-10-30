import ast

# Define a sample recursive function
code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""

# Parse the code into an AST
tree = ast.parse(code)

# Define a custom NodeVisitor to handle function nodes
class RecursiveFunctionVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print("Function Name:", node.name)
        print("Function Body:")
        for statement in node.body:
            # Walk through the function body recursively
            ast.walk(statement)
            # Check if there is a recursive call with n = 5
            if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
                func_name = statement.value.func.id
                if func_name == "factorial":
                    arg_value = statement.value.args[0].n
                    if arg_value == 5:
                        print("Recursive call with n = 5 found!")

# Create an instance of the custom visitor
visitor = RecursiveFunctionVisitor()

# Visit and print information about functions in the code
visitor.visit(tree)
