import numpy as np
import ast
import astunparse
import sys
sys.path.append("..") 
from CodeToSicclConverter import CodeToSicclConverter


if __name__ == "__main__":
    example_code = open("test_programs/simple_webserver.py", "r").read()

    # print(example_code)
    converter = CodeToSicclConverter()
    siccl = converter.convert(example_code)
    print(siccl)