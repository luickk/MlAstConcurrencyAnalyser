import numpy as np
import sys
sys.path.append("..") 
from SicclToCodeGenerator import SicclToCodeGenerator

if __name__ == "__main__":
    #   thread id, parent arr, var id, mutex id
    siccl_example_flattened = np.array([[1, 0, 2, 2],
                                        [1, 0, 3, 3],
                                        [5, 1, 2, 2], 
                                        [5, 1, 3, 3], 
                                        [6, 5, 2, 2], 
                                        [6, 5, 3, 3], 
                                        [7, 5, 2, 2]], dtype=int)

    # #   thread id, parent arr, var id, mutex id
    # siccl_example_flattened = np.array([[1, 0, 2, 0],
    #                                     [1, 0, 3, 0],
    #                                     [5, 1, 2, 0], 
    #                                     [5, 1, 3, 0], 
    #                                     [6, 5, 2, 0], 
    #                                     [6, 5, 3, 0], 
    #                                     [7, 5, 2, 0]], dtype=int)

    gen = SicclToCodeGenerator(1)
    text = gen.generate(siccl_example_flattened)
    f = open("generated_siccl_example.py",'w')
    print(text)
    f.write(text)
    f.close()

    # print(text)
    