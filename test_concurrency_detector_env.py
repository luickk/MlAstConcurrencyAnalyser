import numpy as np
from concurrency_detector_env import ConcurrencyDetectorEnvironment

if __name__ == "__main__":
	#   parent arr, thread name, var name, mutex name
	siccl_example_flattened = np.array([[0, 1, 2, 2],
	                                    [0, 1, 3, 3],
	                                    [1, 5, 2, 2], 
	                                    [1, 5, 3, 3], 
	                                    [5, 6, 2, 2], 
	                                    [5, 6, 3, 3], 
	                                    [5, 7, 2, 2]], dtype=int)
	env = ConcurrencyDetectorEnvironment(siccl_example_flattened, 1)
	print(env.step((5, 2, 12)))
	# print(env.input_shape)
	# print(env.action_shape)
	# print(env.siccl_arr)
	# print(env.res_text)