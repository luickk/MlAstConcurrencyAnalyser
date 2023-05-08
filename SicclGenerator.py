from random import randint
import numpy as np
import string
import utils
import sys

sys.setrecursionlimit(100000)

# up front: this has to be rewritten and is one of the most inefficient things I've ever done. 
class CodeGeneratorBackend:
    def __init__(self):
        self.code: list[string] = []
        self.tab = "    "
        self.level = 0
    def reset(self):
        self.code = []

    def end(self):
        return "".join(self.code)

    def write(self, string):
        self.code.append(self.tab * self.level + string)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            return
        self.level = self.level - 1

class SicclGenerator():
    def __init__(self, siccl_config_test_time: int):
        self.backend: CodeGeneratorBackend = CodeGeneratorBackend()
        self.known_vars: list[int] = []
        self.known_mutexe: list[int] = []
        self.thread_pgraph: list[list[int, list[int]]] = []
        self.siccl_config_test_time = siccl_config_test_time
    def reset(self):
        self.known_vars = []
        self.known_mutexe = []
        self.thread_pgraph = []

    def end_loops_timer_thread(self):
        self.backend.dedent()
        self.backend.write('\n')
        self.backend.write('def end_loops_timer_thread():\n')
        self.backend.indent()
        self.backend.write('time.sleep({0})\n'.format(self.siccl_config_test_time))
        self.backend.write('globals()["exit_loops"] = True\n')
        
        self.backend.write('time.sleep(0.5)\n')

        self.backend.write('shared_vars_count: dict[int, int] = {}\n')
        stringified_thread_dgraph = utils.print_to_string(self.thread_pgraph_flat)
        self.backend.write('thread_pgraph = {0}\n'.format(stringified_thread_dgraph))
        self.backend.write('for thread, params in thread_pgraph.items():\n')
        self.backend.indent()
        self.backend.write('for dgraph_var in params:\n')
        self.backend.indent()
        self.backend.write('if dgraph_var in shared_vars_count:\n')
        self.backend.indent()
        self.backend.write('shared_vars_count[dgraph_var] += per_thread_loop_count[thread]\n')
        self.backend.dedent()
        self.backend.write('else:\n')
        self.backend.indent()
        self.backend.write('shared_vars_count[dgraph_var] = per_thread_loop_count[thread]\n')
        self.backend.dedent()
        self.backend.dedent()
        self.backend.dedent()

        self.backend.write('for i, (key, val) in enumerate(end_loop_shared_vars_res.items()): \n')
        self.backend.indent()
        self.backend.write('if key in shared_vars_count:\n')
        self.backend.indent()
        self.backend.write('average = sum(val) / len(val)\n')
        self.backend.write('print(str(key) + ":" + str(shared_vars_count[key]-average))\n')
        self.backend.dedent()
        self.backend.dedent()
        self.backend.write('\n')
        
        self.backend.write('\n')
        
        self.backend.dedent()
        self.backend.write('\n')

    def create_main(self, siccl_array):
        self.backend.write('#!/usr/bin/python3\n')
        self.backend.write('\n')
        self.backend.write('import threading\n')
        self.backend.write('import time\n')
        self.backend.write('from threading import Thread\n')
        self.backend.write('\n')
        self.backend.write("exit_loops = False\n")
        self.backend.write("end_loop_shared_vars_res: dict[int, list[int]] = {}\n")
        highest_thread_id = 0
        for elem in siccl_array:
            if elem[1] > highest_thread_id:
                highest_thread_id = elem[1]
        self.backend.write("per_thread_loop_count = [0]*{0}\n".format(highest_thread_id+1))
        self.end_loops_timer_thread()
        self.backend.write('def main():\n')
        self.backend.indent()

        for elem in siccl_array:
            if elem[0] == 0 and elem[1] == 1:
                self.backend.write('var_{0} = [{1}, {2}]\n'.format(elem[2], 0, 0))

        self.backend.write('arguments = locals()\n')
        self.backend.write('loop_stop_thread = Thread(target=end_loops_timer_thread, args=()) \n')
        self.backend.write('loop_stop_thread.start()\n')

    def call_main(self):
        self.backend.dedent()
        self.backend.dedent()
        self.backend.write('\n')
        self.backend.write('if __name__ == "__main__":\n')
        self.backend.indent()
        self.backend.write('main()\n')
    def create_thread(self, name: string, params: list[int]):
        params = utils.remove_dup(params)
        self.backend.dedent()
        self.backend.write('\n')
        stringiefied_t_params = params.copy()
        for i, param in enumerate(stringiefied_t_params):
            stringiefied_t_params[i] = "var_" + str(param)
        self.backend.write('def thread_{0}({1}):\n'.format(str(name), ", ".join(stringiefied_t_params)))
        self.backend.indent()
        self.backend.write('arguments = locals()\n')

    def traverse_tree(self, root_call: bool, siccl_array: np.array, thread_dgraph: dict[list[int, list[int]]], thread_dgraph_full: dict[list[int, list[int]]], thread_mgraph: dict[list[int, list[int]]], thread_pgraph: dict[tuple[int, list[int]]]) -> None:
        inited_mutexe: list[int] = []
        last_thread_name = 0
        for i_siccl_arr, var in enumerate(siccl_array):
            mutex_name = var[3]
            var_name = var[2]
            thread_name = var[1]
            parent_thread = var[0]
            # new thread
            if last_thread_name != thread_name:
                self.backend.dedent()
                if root_call: 
                    self.create_main(siccl_array);
                    root_call = False
                else: 
                    thread_params: list[int] = []
                    if thread_name in thread_pgraph:
                        thread_params = thread_pgraph[thread_name]
                    self.create_thread(thread_name, thread_params);

                if thread_name in thread_dgraph:
                    for curr_thread_mutex in thread_mgraph[thread_name]:
                        if curr_thread_mutex != 0:
                            if curr_thread_mutex not in self.known_mutexe:
                                self.backend.write("global mutex_{0}\n".format(curr_thread_mutex))
                                self.backend.write("mutex_{0} = threading.Lock()\n".format(curr_thread_mutex))
                                self.known_mutexe.append(curr_thread_mutex)
                    for dependant_thread in thread_dgraph[thread_name]:
                        if dependant_thread in thread_mgraph:
                            for next_thread_mutex in thread_mgraph[dependant_thread]:
                                if next_thread_mutex != 0:
                                    if next_thread_mutex not in self.known_mutexe:
                                        self.backend.write("global mutex_{0}\n".format(next_thread_mutex))
                                        self.backend.write("mutex_{0} = threading.Lock()\n".format(next_thread_mutex))
                                        self.known_mutexe.append(next_thread_mutex)
                        thread_params: list[int] = []
                        if dependant_thread in thread_pgraph:
                            thread_params = thread_pgraph[dependant_thread]
                        
                        stringiefied_t_params = utils.remove_dup(thread_params)
                        for i, param in enumerate(stringiefied_t_params):
                            stringiefied_t_params[i] =  "var_" + str(param)
                            if param not in self.known_vars:
                                self.backend.write('var_{0} = [{1}, {2}]\n'.format(param, 0, 0))
                                self.known_vars.append(param)
                        self.backend.write('t_{0} = Thread(target=thread_{0}, args=({1},)) \n'.format(str(dependant_thread), ", ".join(stringiefied_t_params)))
                        self.backend.write('t_{0}.start()\n'.format(str(dependant_thread)))

                self.backend.write('while not exit_loops:\n')
                self.backend.indent()
                self.backend.write('per_thread_loop_count[{0}] += 1\n'.format(thread_name))
                
            # self.backend.write('print("?")\n')
            if var_name in self.known_vars:
                if mutex_name != 0:
                    if mutex_name not in self.known_mutexe:
                        self.backend.write("global mutex_{0}\n".format(mutex_name))
                        self.backend.write("mutex_{0} = threading.Lock()\n".format(mutex_name))
                        self.known_mutexe.append(mutex_name)
                    self.backend.write("mutex_{0}.acquire()\n".format(mutex_name))

                self.backend.write('var_{0}[0] += 1\n'.format(var_name))

                if mutex_name != 0:
                    self.backend.write("mutex_{0}.release()\n".format(mutex_name))
            if i_siccl_arr < len(siccl_array)-1 and siccl_array[i_siccl_arr+1][1] != thread_name or i_siccl_arr == len(siccl_array)-1:
                self.backend.dedent()
                self.backend.write('arguments_list = arguments.items()\n')
                self.backend.write('params = []\n')
                self.backend.write('for key, val in arguments_list: params.append(int(key.split("_")[1]))\n')
                self.backend.write('for i, param in enumerate(params):\n')
                self.backend.indent()
                self.backend.write('if arguments["var_" + str(param)][0] != 0: \n')
                self.backend.indent()
                self.backend.write('if param in end_loop_shared_vars_res:\n'.format(thread_name))
                self.backend.indent()
                self.backend.write('end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])\n')
                self.backend.dedent()
                self.backend.write('else:\n')
                self.backend.indent()
                self.backend.write('end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]\n')
                self.backend.dedent()
                self.backend.dedent()
            
            last_thread_name = thread_name
    # list threads with its threads (dependencies)
    def generate_thread_tokenized_graph(self, siccl_array: np.array) -> dict[int, list[int]]:
        thread_dgraph_tokenized: dict[int, list[int]] = {}

        last_thread_name = 0
        for i, elem in enumerate(siccl_array):
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]

            if last_thread_name != thread_name:
                if parent_thread in thread_dgraph_tokenized:
                    if thread_name not in thread_dgraph_tokenized[parent_thread]:
                        thread_dgraph_tokenized[parent_thread].append(thread_name)
                else:
                    thread_dgraph_tokenized[parent_thread] = [thread_name]

            last_thread_name = thread_name

        for i, elem in enumerate(siccl_array):
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]
            if thread_name not in thread_dgraph_tokenized:
                thread_dgraph_tokenized[thread_name] = []

        return thread_dgraph_tokenized

    def generate_full_thread_dependency_graph(self, thread_dgraph_comp: list[int], thread_dgraph_tokenized: dict[int, list[int]], to_look_up_thread: int) -> dict[int, list[int]]:
        if to_look_up_thread in thread_dgraph_tokenized:
            dependant_threads = thread_dgraph_tokenized[to_look_up_thread]
            
            for i, dp in enumerate(dependant_threads):
                if dp not in thread_dgraph_comp:
                    thread_dgraph_comp.append(dp)
                self.generate_full_thread_dependency_graph(thread_dgraph_comp, thread_dgraph_tokenized, dp)
        return thread_dgraph_comp

    def gen_dep_graphs(self, siccl_array):
        thread_dgraph = {}
        thread_dgraph_tokenized = self.generate_thread_tokenized_graph(siccl_array)
        # print("tokenized draph: ", thread_dgraph_tokenized)
        for thread_name, dependant_threads in thread_dgraph_tokenized.items():
            tmp_graph = []
            if thread_name not in thread_dgraph:
                thread_dgraph[thread_name] = []
            thread_dgraph[thread_name].extend(self.generate_full_thread_dependency_graph(tmp_graph, thread_dgraph_tokenized, thread_name))
        return thread_dgraph_tokenized, thread_dgraph

    def get_threads_params(siccl_array: np.array, thread_name: int) -> list[int]:        
        res: list[int] = []
        for i, elem in enumerate(siccl_array):
            # print()
            if elem[1] == thread_name:
                res.append(elem[2])
        return res

    def get_threads_mutexe(siccl_array: np.array, thread_name: int) -> list[int]:        
        res: list[int] = []
        for i, elem in enumerate(siccl_array):
            # print()
            if elem[1] == thread_name:
                res.append(elem[3])
        return res

    # list threads with its parameters (variables required/ share)
    def generate_thread_params_graph(self, siccl_array: np.array, dependency_graph: dict[int, list[int]]) -> dict[int, list[int]]:
        thread_pgraph: dict[int, list[int]] = {}
        for thread_name, dependant_threads in dependency_graph.items():
            dependant_threads = dependant_threads.copy()
            thread_pgraph[thread_name] = []
            if len(dependant_threads) == 0:
                params = SicclGenerator.get_threads_params(siccl_array, thread_name)
                thread_pgraph[thread_name].extend(params)
            if thread_name not in dependant_threads:
                dependant_threads.append(thread_name)
            for dt in dependant_threads:
                params = SicclGenerator.get_threads_params(siccl_array, dt)
                thread_pgraph[thread_name].extend(params)

        return thread_pgraph

    # list threads with its mutexe
    def generate_thread_mutex_graph(self, siccl_array: np.array, dependency_graph: dict[int, list[int]]) -> dict[int, list[int]]:
        thread_mutex_graph: dict[int, list[int]] = {}
        for thread_name, dependant_threads in dependency_graph.items():
            thread_mutex_graph[thread_name] = []
            for dt in dependant_threads:
                mutexe = SicclGenerator.get_threads_mutexe(siccl_array, dt)
                thread_mutex_graph[thread_name].extend(mutexe)
        return thread_mutex_graph

    # probably one of the most inefficient thing I've ever written...
    def generate(self, siccl_array: list) -> string:
        self.backend.reset()
        self.reset()
        thread_dgraph, thread_dgraph_full = self.gen_dep_graphs(siccl_array)
        thread_mgraph = self.generate_thread_mutex_graph(siccl_array, thread_dgraph)
        self.thread_pgraph = self.generate_thread_params_graph(siccl_array, thread_dgraph_full)
        self.thread_pgraph_flat = self.generate_thread_params_graph(siccl_array, thread_dgraph)
        print("dgrpah:", thread_dgraph)
        print("dgrpah full:", thread_dgraph_full)
        print("mgraph: ", thread_mgraph)
        print("pgraph: ", self.thread_pgraph_flat)
        print("pgraph full: ", self.thread_pgraph)
        self.traverse_tree(True, siccl_array, thread_dgraph, thread_dgraph_full, thread_mgraph, self.thread_pgraph)
        self.call_main();
        return self.backend.end()
