from SicclGenerator import SicclGenerator
import itertools
import numpy as np
import utils
import pandas as pd
class ConcurrencyDetectorEnvironment:
	# siccl_example = ["var1_m1", "var2", ["var1_m1", "var2_m1"], ["var1_m1","var2"], ["var3","var2"]] # old version
	siccl_example_flattened = np.array([["main", "thread1", "var1", "m1"], 
										["main", "thread1", "var2", ""], 
										["thread1", "thread2", "var1", "m1"], 
										["thread1", "thread2", "var1", "m1"], 
										["thread1", "thread3", "var1", "m1"]], dtype=object)

	def __init__(self, siccl_arr: np.array=None):
		if siccl_arr == None: 
			siccl_arr = ConcurrencyDetectorEnvironment.siccl_example_flattened
		else: 
			siccl_arr = siccl_arr
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