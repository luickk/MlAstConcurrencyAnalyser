from SicclGenerator import SicclGenerator
import utils

class ConcurrencyDetectorEnvironment:
	siccl_example = ["var1_m1", "var2", "var3", ["var1_m1"], ["var1_m1","var2", ["var2", ["var3","var1"]]], ["var3","var2"]]

	def __init__(self, siccl_list=None):
		if siccl_list == None: siccl_list = ConcurrencyDetectorEnvironment.siccl_example
		self.siccl_list = siccl_list
		self.gen: SicclGenerator= SicclGenerator()
		self.res_text: list[str] = []

	# action tuple: action, index, mutex name
	def step(self, action: (int, list, str)):
		# add mutex
		if action[0] == 1:
			var_name = utils.index_multi_dim_multi_axis_list(self.siccl_list, action[1])
			if var_name != None or isinstance(var_name, str):
				if utils.parse_var(var_name)[1] == None:
					utils.index_multi_dim_multi_axis_list(self.siccl_list, action[1], var_name + "_" + action[2])
		# remove mutex
		if action[0] == 2:
			var_name = utils.index_multi_dim_multi_axis_list(self.siccl_list, action[1])
			if var_name != None or isinstance(var_name, str):
				if utils.parse_var(var_name)[1] != None:
					utils.index_multi_dim_multi_axis_list(self.siccl_list, action[1], var_name.split("_")[0])

		self.res_text = self.gen.generate(self.siccl_list)

	def reset(self):
		self.siccl_list = siccl_example
	    
	
	def save_env(self):
		f = open("generated_siccl_example.py",'w')
		f.write(self.res_text)
		f.close()