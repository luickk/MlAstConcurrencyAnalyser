from concurrency_detector_env import ConcurrencyDetectorEnvironment
from enum import Enum 


if __name__ == "__main__":
	env = ConcurrencyDetectorEnvironment()

	env.step((1, [4, 1], "peter"))
	print(env.siccl_list)
	print(env.res_text)