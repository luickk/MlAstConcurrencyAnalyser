from concurrency_detector_env import ConcurrencyDetectorEnvironment

if __name__ == "__main__":
	env = ConcurrencyDetectorEnvironment()
	print(env.input_shape)
	env.step((1, 2, 12))
	
	print(env.siccl_list)
	print(env.res_text)