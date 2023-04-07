from SicclGenerator import SicclGenerator
import itertools
import numpy as np
import utils
import pandas as pd
import sys
from io import StringIO
import contextlib


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class ConcurrencyDetectorEnvironment:
	def __init__(self, siccl_arr: np.array):
		self.reset_env = siccl_arr
		self.siccl_arr = siccl_arr
		self.n_action = 1
		self.gen: SicclGenerator= SicclGenerator()
		self.res_text: list[str] = []
		self.input_shape = self.siccl_arr.shape
		self.action_shape = (4,)

	# action tuple: action, index, mutex id
	def step(self, action: (int, int, int)):
		index = np.unravel_index(action[1], self.siccl_arr.shape)[0]
		mutex_name = self.siccl_arr[index][3]
		var_name = self.siccl_arr[index][2]
		thread_name = self.siccl_arr[index][1]
		parent_thread = self.siccl_arr[index][0]
		# add mutex
		if action[0] == 0:
			self.siccl_arr[index][3] = str(action[2])
		# remove mutex
		if action[0] == 1:
			self.siccl_arr[index][3] = 0

		self.res_text = self.gen.generate(self.siccl_arr)

		reward = 0
		with stdoutIO() as s:
			try:
			    exec(self.res_text)
			except:
			    # state, reward, done
				return self.siccl_arr, -10, False
		reward = 1
		# state, reward, done
		return self.siccl_arr, reward, False

		

	def reset(self):
		self.siccl_arr = self.reset_env
		return self.siccl_arr
	
	def save_env(self):
		f = open("generated_siccl_example.py",'w')
		f.write(self.res_text)
		f.close()