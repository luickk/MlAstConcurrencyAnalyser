from SicclToCodeGenerator import SicclToCodeGenerator
import itertools
import numpy as np
import os
import utils
import pandas as pd
import sys
from io import StringIO
import contextlib
import subprocess


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class ConcurrencyDetectorEnvironment:
	def __init__(self, siccl_arr: np.array, siccl_config_test_time: int):
		self.reset_env = siccl_arr
		self.siccl_arr = siccl_arr
		self.n_action = 1
		self.gen: SicclToCodeGenerator= SicclToCodeGenerator(siccl_config_test_time)
		self.res_text: list[str] = []
		self.input_shape = self.siccl_arr.shape
		self.action_shape = (4,)
		self.last_reward = 0

	# action tuple: index, mutex id
	def step(self, action: (int, int)):
		index = action[0]
		mutex_name = self.siccl_arr[index][3]
		var_name = self.siccl_arr[index][2]
		parent_thread = self.siccl_arr[index][1]
		thread_name = self.siccl_arr[index][0]
		# add mutex
		# if action[0] == 1:
		self.siccl_arr[index][3] = str(action[1])
		# # remove mutex
		# if action[0] == 0:
		# 	self.siccl_arr[index][3] = 0

		self.res_text = self.gen.generate(self.siccl_arr)

		reward = 0
		# print(self.res_text)

		ok_rc = subprocess.Popen(['python3', '-c', self.res_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output =  ok_rc.stdout.read()
		err_outp = ok_rc.stderr.read()
		ok_rc.communicate()

		if len(err_outp) == 0:
			output = output.decode("utf-8").split("\n")
			for res in output:
				split_res = res.split(":")
				if len(split_res) == 2:
					print("+ ", float(split_res[1]))
					reward += float(split_res[1])
		else:
			print("crahs!?: ", err_outp)
			reward = 6000000
		reward = 1 - utils.map_value(reward, 0, 3, 0, 1)
		print("absoult: " + str(reward))
		reward = reward - self.last_reward
		if reward < 0: reward = 0
		print(str(reward) + "-" + str(self.last_reward))
		print("reward: " + str(reward))
		self.last_reward = reward
		# state, reward, done
		return self.siccl_arr, reward, False

		

	def reset(self):
		self.siccl_arr = self.reset_env
		return self.siccl_arr
	
	def save_env(self):
		f = open("generated_siccl_example.py",'w')
		f.write(self.res_text)
		f.close()
		
		