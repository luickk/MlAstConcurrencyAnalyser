import numpy as np
from concurrency_detector_env import ConcurrencyDetectorEnvironment

if __name__ == "__main__":
	#   parent arr, thread name, var name, mutex name
	siccl_example_flattened = np.array([[0, 1, 2, 6],
										 [0, 1, 3, 4],
										 [1, 5, 2, 1],
										 [1, 5, 3, 0],
										 [5, 6, 2, 0],
										 [5, 6, 3, 4],
										 [5, 7, 2, 4]], dtype=int)
	env = ConcurrencyDetectorEnvironment(siccl_example_flattened, 1)
	# action tuple: action, index, mutex id
	print(env.step((1, 5, 12)))
	# print(env.input_shape)
	# print(env.action_shape)
	# print(env.siccl_arr)
	# print(env.res_text)