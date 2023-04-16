from random import randint
import numpy as np
import string
import utils


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

        self.backend.write('shared_vars_count: list[int, int] = []\n')
        stringified_thread_dgraph = utils.print_to_string(self.thread_pgraph)
        self.backend.write('thread_pgraph = {0}\n'.format(stringified_thread_dgraph))
        self.backend.write('for i_thread, thread in enumerate(thread_pgraph):\n')
        self.backend.indent()
        self.backend.write('for dgraph_var in thread[1]:\n')
        self.backend.indent()
        self.backend.write('found = False\n')
        self.backend.write('for var_count in shared_vars_count:\n')
        self.backend.indent()
        self.backend.write('if dgraph_var == var_count[0]:\n')
        self.backend.indent()
        self.backend.write('found = True\n')
        self.backend.write('var_count[1] += per_thread_loop_count[thread[0]]\n')
        self.backend.dedent()
        self.backend.dedent()
        self.backend.write('if not found:\n')
        self.backend.indent()
        self.backend.write('shared_vars_count.append([dgraph_var, per_thread_loop_count[thread[0]]])\n')
        self.backend.dedent()
        self.backend.dedent()
        self.backend.dedent()
        

        # self.backend.write('print(per_thread_loop_count)\n')
        # self.backend.write('print(shared_vars_count)\n')
        # self.backend.write('print(end_loop_shared_vars_res)\n')
        self.backend.write('assert(len(shared_vars_count) == len(end_loop_shared_vars_res))\n')
        self.backend.write('for i, var in enumerate(end_loop_shared_vars_res): \n')
        self.backend.indent()
        self.backend.write('average = sum(var[1]) / len(var[1])\n')
        self.backend.write('print(str(var[0]) + ":" + str(shared_vars_count[i][1]-average))\n')
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
        self.backend.write("end_loop_shared_vars_res: list[int, list[int]] = []\n")
        highest_thread_id = 0
        for elem in siccl_array:
            if elem[1] > highest_thread_id:
                highest_thread_id = elem[1]
        self.backend.write("per_thread_loop_count = [0]*{0}\n".format(highest_thread_id+1))
        self.end_loops_timer_thread()
        self.backend.write('def main():\n')
        self.backend.indent()
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
        self.backend.dedent()
        self.backend.write('\n')
        stringiefied_t_params = params.copy()
        for i, param in enumerate(stringiefied_t_params):
            stringiefied_t_params[i] = "var_" + str(param)
        self.backend.write('def thread_{0}({1}):\n'.format(str(name), ", ".join(stringiefied_t_params)))
        self.backend.indent()
        self.backend.write('arguments = locals()\n')

    def traverse_tree(self, root_call: bool, siccl_array: np.array, thread_dgraph: list[list[int, list[int]]], thread_mgraph: list[list[int, list[int]]], thread_pgraph: list[tuple[int, list[int]]]) -> None:
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
                    for params_per_thread in thread_pgraph:
                        if params_per_thread[0] == thread_name:
                            thread_params = params_per_thread[1]
                    self.create_thread(thread_name, thread_params);


                for deps_per_thread in thread_dgraph:
                    if deps_per_thread[0] == thread_name:
                        for dependant_thread in deps_per_thread[1]:
                            for mutexe_per_thread in thread_mgraph:                
                                if mutexe_per_thread[0] == dependant_thread:
                                    for next_thread_mutex in mutexe_per_thread[1]:
                                        if mutex_name != 0:
                                            if next_thread_mutex not in self.known_mutexe:
                                                self.backend.write("global mutex_{0}\n".format(next_thread_mutex))
                                                self.backend.write("mutex_{0} = threading.Lock()\n".format(next_thread_mutex))
                                                self.known_mutexe.append(next_thread_mutex)
                            thread_params: list[int] = []
                            for params_per_thread in thread_pgraph:
                                if params_per_thread[0] == dependant_thread:
                                    thread_params = params_per_thread[1]


                            stringiefied_t_params = thread_params.copy()
                            for i, param in enumerate(stringiefied_t_params):
                                stringiefied_t_params[i] =  "var_" + str(param)
                                if param not in self.known_vars:
                                    self.backend.write('var_{0} = [{1}, {2}]\n'.format(param, randint(0, 100), randint(0, 100)))
                                    self.known_vars.append(param)
                            self.backend.write('t_{0} = Thread(target=thread_{0}, args=({1},)) \n'.format(str(dependant_thread), ", ".join(stringiefied_t_params)))
                            self.backend.write('t_{0}.start()\n'.format(str(dependant_thread)))


                self.backend.write('while not exit_loops:\n')
                self.backend.indent()
                self.backend.write('per_thread_loop_count[{0}] += 1\n'.format(thread_name))
                
            # self.backend.write('print("?")\n')
            if var_name in self.known_vars:
                if mutex_name != 0:
                    self.backend.write("mutex_{0}.acquire()\n".format(mutex_name))

                self.backend.write('var_{0}[0] += 1\n'.format(var_name))

                if mutex_name != 0:
                    self.backend.write("mutex_{0}.release()\n".format(mutex_name))

            if i_siccl_arr < len(siccl_array)-1 and siccl_array[i_siccl_arr+1][1] != thread_name:
                self.backend.dedent()
                self.backend.write('arguments_list = arguments.items()\n')
                self.backend.write('params = []\n')
                self.backend.write('for key, val in arguments_list: params.append(int(key.split("_")[1]))\n')
                self.backend.write('for i, param in enumerate(params):\n')
                self.backend.indent()
                self.backend.write('found = False\n')
                self.backend.write('for elem in end_loop_shared_vars_res:\n'.format(thread_name))
                self.backend.indent()
                self.backend.write('if elem[0] == param:\n')
                self.backend.indent()
                self.backend.write('found = True\n')
                self.backend.write('elem[1].append(arguments["var_" + str(param)][0])\n')
                self.backend.dedent()
                self.backend.dedent()
                self.backend.write('if not found:\n')
                self.backend.indent()
                self.backend.write('end_loop_shared_vars_res.append([param, [arguments["var_" + str(param)][0]]])\n')
                self.backend.dedent()
            
            last_thread_name = thread_name
    # list threads with its threads (dependencies)
    def generate_thread_dependency_graph(self, siccl_array: np.array) -> list[list[int, list[int]]]:
        thread_dgraph: list[int, list[int]] = []

        last_thread_name = 0
        for i, elem in enumerate(siccl_array):
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]

            if last_thread_name != thread_name:
                i = 0
                found = False
                for i, node in enumerate(thread_dgraph):
                    if node[0] == parent_thread:
                        found = True
                        if thread_name not in node[1]:
                            node[1].append(thread_name)
                if not found:
                    thread_dgraph.append((parent_thread, [thread_name]))

            last_thread_name = thread_name

        return thread_dgraph


    def get_threads_params(siccl_array: np.array, thread_name: int) -> list[int]:        
        res: list[int] = []
        for i, elem in enumerate(siccl_array):
            # print()
            if elem[1] == thread_name:
                if elem[2] not in res:
                    res.append(elem[2])
        return res

    # list threads with its parameters (variables required/ share)
    def generate_thread_params_graph(self, siccl_array: np.array) -> list[list[int, list[int]]]:
        thread_pgraph: list[int, list[int]] = []
        last_thread_name = 0
        for i, elem in enumerate(siccl_array):
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]
            
            i = 0
            params = SicclGenerator.get_threads_params(siccl_array, thread_name)
            # print(params)
            
            if last_thread_name != thread_name:
                thread_pgraph.append((thread_name, params))
            last_thread_name = thread_name
                
            for i, node in enumerate(thread_pgraph):
                if node[0] == parent_thread:
                    node[1].extend(params)
        # it's so ugly, it hurts
        for node in thread_pgraph:
            dups_removed = utils.remove_dup(node[1])
            node[1].clear()
            node[1].extend(dups_removed)
        return thread_pgraph

    # list threads with its mutexe
    def generate_thread_mutex_graph(self, siccl_array: np.array) -> list[list[int, list[int]]]:
        thread_mutex_graph: list[int, list[int]] = []

        for i, elem in enumerate(siccl_array):
            mutex_name = elem[3]
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]
            found = False

            for i, node in enumerate(thread_mutex_graph):
                if thread_name == node[0]:
                    found = True
                    if mutex_name not in node[1] and mutex_name != 0:
                        node[1].append(mutex_name)
            if not found:
                thread_mutex_graph.append((thread_name, [mutex_name]))

        return thread_mutex_graph

    # probably one of the most inefficient thing I've ever written...
    def generate(self, siccl_array: list) -> string:
        self.backend.reset()
        self.reset()
        # generating the graphs seperately is a (great)bit more inefficient but more readable
        thread_dgraph = self.generate_thread_dependency_graph(siccl_array)
        thread_mgraph = self.generate_thread_mutex_graph(siccl_array)
        self.thread_pgraph = self.generate_thread_params_graph(siccl_array)
        self.traverse_tree(True, siccl_array, thread_dgraph, thread_mgraph, self.thread_pgraph)
        self.call_main();
        return self.backend.end()
