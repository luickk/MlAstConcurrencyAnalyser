import numpy as np
from SicclGenerator import SicclGenerator

if __name__ == "__main__":
    #   parent arr, thread name, var name, mutex name
    # siccl_example_flattened = np.array([[0, 1, 2, 2],
    #                                     [0, 1, 3, 3],
    #                                     [1, 5, 2, 2], 
    #                                     [1, 5, 3, 3], 
    #                                     [5, 6, 2, 2], 
    #                                     [5, 6, 3, 3], 
    #                                     [5, 7, 2, 2]], dtype=int)

    # #   parent arr, thread name, var name, mutex name
    siccl_example_flattened = np.array([[0, 1, 2, 0],
                                        [0, 1, 3, 0],
                                        [1, 5, 2, 0], 
                                        [1, 5, 3, 0], 
                                        [5, 6, 2, 0], 
                                        [5, 6, 3, 0], 
                                        [5, 7, 2, 0]], dtype=int)
    gen = SicclGenerator(1)
    text = gen.generate(siccl_example_flattened)
    f = open("generated_siccl_example.py",'w')
    f.write(text)
    f.close()

    # print(text)
    