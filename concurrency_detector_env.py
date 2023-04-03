from SicclGenerator import SicclGenerator
import itertools
import numpy as np
import utils
import pandas as pd
class ConcurrencyDetectorEnvironment:
	def __init__(self, siccl_arr: np.array):
		self.reset_env = siccl_arr
		self.siccl_arr = siccl_arr
		self.gen: SicclGenerator= SicclGenerator()
		self.res_text: list[str] = []
		self.input_shape = self.siccl_arr.shape

	# action tuple: action, (multi dim)index, mutex id
	def step(self, action: (int, list, int)):
		index = action[1]
		mutex_name = self.siccl_arr[index][3]
		var_name = self.siccl_arr[index][2]
		thread_name = self.siccl_arr[index][1]
		parent_thread = self.siccl_arr[index][0]
		# add mutex
		if action[0] == 1:
			self.siccl_arr[index][3] = str(action[2])
		# remove mutex
		if action[0] == 2:
			self.siccl_arr[index][3] = ""

		self.res_text = self.gen.generate(self.siccl_arr)

	def reset(self):
		self.siccl_arr = self.r
	
	def save_env(self):
		f = open("generated_siccl_example.py",'w')
		f.write(self.res_text)
		f.close()