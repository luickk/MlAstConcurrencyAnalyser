import numpy as np
import sys
sys.path.append("..") 
from RandomSicclGenerator import RandomSicclGenerator

if __name__ == "__main__":
    gen = RandomSicclGenerator(10, 2)

    siccl = gen.generate()
    print(repr(siccl))