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

    siccl_example_flattened = np.array([[0, 1, 1, 0], [0, 1, 3, 0], [0, 1, 5, 0], [0, 1, 1, 0], [0, 1, 7, 0], [0, 1, 1, 2], [0, 1, 9, 0], [1, 2, 11, 0], [1, 2, 13, 0], [1, 3, 14, 0], [1, 3, 7, 0], [1, 3, 1, 2], [1, 3, 9, 0], [3, 4, 2, 0], [3, 4, 0, 1], [3, 4, 8, 0], [3, 4, 10, 0], [3, 5, 7, 0], [3, 5, 8, 0], [3, 5, 10, 0]], dtype=int)
    gen = SicclGenerator(1)
    text = gen.generate(siccl_example_flattened)
    f = open("generated_siccl_example.py",'w')
    f.write(text)
    f.close()

    # print(text)
    