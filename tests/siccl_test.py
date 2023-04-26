import numpy as np
import sys
sys.path.append("..") 
from SicclGenerator import SicclGenerator

if __name__ == "__main__":
    #   parent arr, thread id, var id, mutex id
    siccl_example_flattened = np.array([[0, 1, 2, 2],
                                        [0, 1, 3, 3],
                                        [1, 5, 2, 2], 
                                        [1, 5, 3, 3], 
                                        [5, 6, 2, 2], 
                                        [5, 6, 3, 3], 
                                        [5, 7, 2, 2]], dtype=int)

    # #   parent arr, thread id, var id, mutex id
    # siccl_example_flattened = np.array([[0, 1, 2, 0],
    #                                     [0, 1, 3, 0],
    #                                     [1, 5, 2, 0], 
    #                                     [1, 5, 3, 0], 
    #                                     [5, 6, 2, 0], 
    #                                     [5, 6, 3, 0], 
    #                                     [5, 7, 2, 0]], dtype=int)

    # siccl_example_flattened = np.array([[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 2, 0], [0, 1, 3, 0], [0, 1, 4, 0], [0, 1, 2, 0], [0, 1, 5, 0], [0, 1, 6, 0], [0, 1, 7, 0], [0, 1, 6, 0], [0, 1, 8, 0], [0, 1, 9, 0], [0, 1, 10, 0], [0, 1, 3, 0], [0, 1, 11, 0], [0, 1, 8, 0], [0, 1, 9, 0], [0, 1, 10, 0], [0, 1, 12, 0], [0, 1, 13, 0], [0, 1, 5, 1], [0, 1, 8, 0], [0, 1, 5, 0], [0, 1, 7, 2], [0, 1, 9, 0], [0, 1, 7, 0], [0, 1, 14, 0], [0, 1, 0, 0], [0, 1, 15, 0], [0, 1, 16, 0], [0, 1, 17, 0], [0, 1, 14, 0], [0, 1, 15, 0], [0, 1, 18, 0], [0, 1, 16, 0], [0, 1, 19, 0], [0, 1, 20, 0], [0, 1, 21, 0], [0, 1, 15, 0], [0, 1, 22, 0], [0, 1, 23, 0], [0, 1, 24, 0], [0, 1, 23, 0], [0, 1, 20, 0], [0, 1, 22, 0], [0, 1, 23, 0], [0, 1, 0, 0], [0, 1, 25, 0], [0, 1, 20, 0], [0, 1, 22, 0], [0, 1, 24, 0], [0, 1, 20, 0], [0, 1, 0, 0], [0, 1, 25, 0], [0, 1, 20, 0], [1, 2, 26, 0], [1, 2, 27, 0], [1, 2, 26, 0], [1, 2, 28, 0], [1, 2, 29, 0], [1, 2, 18, 0], [1, 2, 18, 0], [1, 2, 30, 0], [1, 2, 31, 0], [1, 2, 32, 0], [1, 2, 21, 0], [1, 2, 30, 0], [1, 2, 33, 0], [1, 2, 32, 0], [1, 2, 22, 0], [1, 2, 34, 0], [1, 2, 28, 0], [1, 2, 33, 0], [1, 2, 34, 0], [1, 2, 22, 0], [1, 2, 34, 0], [1, 2, 13, 0], [1, 2, 32, 0], [1, 2, 22, 0], [1, 2, 28, 0], [1, 2, 33, 0], [1, 2, 13, 0], [1, 2, 32, 0], [1, 2, 35, 0], [1, 2, 28, 0], [1, 2, 35, 0], [1, 2, 24, 0], [1, 2, 19, 0], [1, 2, 36, 0], [1, 2, 21, 0], [1, 2, 24, 0], [1, 2, 37, 0], [1, 2, 38, 0], [1, 2, 36, 0], [1, 2, 35, 0], [1, 2, 36, 0], [1, 2, 39, 0], [1, 2, 25, 0], [1, 2, 36, 0], [1, 2, 25, 0], [1, 2, 28, 0], [1, 2, 19, 0], [1, 2, 37, 0], [1, 3, 0, 0], [1, 3, 1, 0], [1, 3, 40, 0], [1, 3, 3, 0], [1, 3, 41, 0], [1, 3, 8, 0], [1, 3, 9, 0], [1, 3, 40, 0], [1, 3, 42, 0], [1, 3, 3, 0], [1, 3, 43, 0], [1, 3, 8, 0], [1, 3, 42, 0], [1, 3, 12, 0], [1, 3, 13, 0], [1, 3, 5, 1], [1, 3, 8, 0], [1, 3, 5, 0], [1, 3, 7, 2], [1, 3, 9, 0], [1, 3, 7, 0], [1, 3, 14, 0], [1, 3, 0, 0], [1, 3, 15, 0], [1, 3, 16, 0], [1, 3, 17, 0], [1, 3, 14, 0], [1, 3, 15, 0], [1, 3, 18, 0], [1, 3, 16, 0], [1, 3, 19, 0], [1, 3, 20, 0], [1, 3, 21, 0], [1, 3, 15, 0], [1, 3, 22, 0], [1, 3, 23, 0], [1, 3, 24, 0], [1, 3, 23, 0], [1, 3, 20, 0], [1, 3, 22, 0], [1, 3, 23, 0], [1, 3, 0, 0], [1, 3, 25, 0], [1, 3, 20, 0], [1, 3, 22, 0], [1, 3, 24, 0], [1, 3, 20, 0], [1, 3, 0, 0], [1, 3, 25, 0], [1, 3, 20, 0], [3, 4, 0, 0], [3, 4, 1, 0], [3, 4, 12, 0], [3, 4, 13, 0], [3, 4, 5, 1], [3, 4, 8, 0], [3, 4, 5, 0], [3, 4, 7, 2], [3, 4, 9, 0], [3, 4, 7, 0], [3, 4, 14, 0], [3, 4, 0, 0], [3, 4, 15, 0], [3, 4, 16, 0], [3, 4, 17, 0], [3, 4, 14, 0], [3, 4, 15, 0], [3, 4, 18, 0], [3, 4, 16, 0], [3, 4, 19, 0], [3, 4, 20, 0], [3, 4, 21, 0], [3, 4, 15, 0], [3, 4, 22, 0], [3, 4, 23, 0], [3, 4, 24, 0], [3, 4, 23, 0], [3, 4, 20, 0], [3, 4, 22, 0], [3, 4, 23, 0], [3, 4, 0, 0], [3, 4, 25, 0], [3, 4, 20, 0], [3, 4, 22, 0], [3, 4, 24, 0], [3, 4, 20, 0], [3, 4, 0, 0], [3, 4, 25, 0], [3, 4, 20, 0], [3, 5, 0, 0], [3, 5, 1, 0], [3, 5, 12, 0], [3, 5, 13, 0], [3, 5, 5, 1], [3, 5, 8, 0], [3, 5, 5, 0], [3, 5, 44, 0], [3, 5, 45, 0]], dtype=int)
    gen = SicclGenerator(1)
    text = gen.generate(siccl_example_flattened)
    f = open("generated_siccl_example.py",'w')
    f.write(text)
    f.close()

    # print(text)
    