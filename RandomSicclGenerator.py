import utils
import random
import numpy as np

class RandomSicclGenerator:
    def __init__(self, n_nodes, n_vars: int):
        self.n_vars = n_vars
        self.curr_thread_counter = 0
        self.curr_var_counter = 0
        self.curr_mutex_counter = 0
        self.curr_column = 0
        self.generated_siccl_arr = np.empty((n_nodes, 4), dtype=int)

    def apply_on_column(self, column):
        n_times = 0
        if self.curr_column == 0:
            for i, elem in enumerate(column):
                if n_times <= 0:
                    n_times = random.randint(1, 5)
                    self.curr_thread_counter += 1
                column[i] = self.curr_thread_counter
                n_times -= 1

        if self.curr_column == 1:
            for i, elem in enumerate(column):
                if n_times <= 0:
                    n_times = random.randint(1, 5)
                column[i] = self.generated_siccl_arr[i][0] - 1
                n_times -= 1

        if self.curr_column == 2:
            for i, elem in enumerate(column):
                column[i] = random.randint(1, self.n_vars)


        if self.curr_column == 3:
            for i, elem in enumerate(column):
                column[i] = 0

        self.curr_column += 1
        return column

    def generate(self):
        res = np.apply_along_axis(self.apply_on_column, axis=0, arr=self.generated_siccl_arr)
        # print(res)
        return res