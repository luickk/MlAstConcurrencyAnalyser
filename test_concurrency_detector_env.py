import numpy as np
from concurrency_detector_env import ConcurrencyDetectorEnvironment

if __name__ == "__main__":
									#	parent arr, thread name, var name, mutex name
	siccl_example_flattened = np.array([["", "main", "var1", "m1"],
										["", "main", "var2", "m1"],
										["main", "thread1", "var1", "m1"], 
										["main", "thread1", "var2", ""], 
										["thread1", "thread2", "var1", "m1"], 
										["thread1", "thread2", "var1", "m1"], 
										["thread1", "thread3", "var1", "m1"]], dtype=object)
	env = ConcurrencyDetectorEnvironment(siccl_example_flattened)
	# print(env.input_shape)
	env.step((5, 2, 12))

	print(env.siccl_arr)
	print(env.res_text)