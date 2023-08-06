import numpy as np
import sys
sys.path.append("..") 
from RandomSicclGenerator import RandomSicclGenerator

if __name__ == "__main__":
    gen = RandomSicclGenerator(200, 10)

    siccl = gen.generate()
    print(repr(siccl))