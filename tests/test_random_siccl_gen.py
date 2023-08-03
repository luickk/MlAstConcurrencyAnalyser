import numpy as np
import sys
sys.path.append("..") 
from RandomSicclGenerator import RandomSicclGenerator

if __name__ == "__main__":
    
    gen = RandomSicclGenerator(20, 5)

    siccl = gen.generate()
    print(siccl)
    