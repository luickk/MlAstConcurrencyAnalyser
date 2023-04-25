import numpy as np
import ast
import astunparse
import sys
sys.path.append("..") 
from code_to_siccl import GenericVisitor
from code_to_siccl import generate_siccle_arr


if __name__ == "__main__":
    example_code = open("generated_siccl_example.py", "r")
    tree = ast.parse(example_code.read())

    visitor = GenericVisitor()
    visitor.visit(tree)

    tokenized_siccl = generate_siccle_arr(visitor.vars_fns, visitor.fn_fns)

    print(tokenized_siccl)