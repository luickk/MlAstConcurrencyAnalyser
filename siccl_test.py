import numpy as np
from SicclGenerator import SicclGenerator

if __name__ == "__main__":
    siccl_example_flattened = np.array([["", "main", "var1", "m1"],
                                        ["", "main", "var2", ""],
                                        ["main", "thread1", "var1", "m1"], 
                                        ["main", "thread1", "var2", ""], 
                                        ["thread1", "thread2", "var1", "m1"], 
                                        ["thread1", "thread2", "var1", "m1"], 
                                        ["thread1", "thread3", "var1", "m1"]], dtype=object)
    gen = SicclGenerator()
    text = gen.generate(siccl_example_flattened)
    f = open("generated_siccl_example.py",'w')
    f.write(text)
    f.close()

    print(text)
    