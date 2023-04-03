from random import randint
import numpy as np
import string
import utils


# up front: this has to be rewritten and is one of the most inefficient things I've ever done. 
class CodeGeneratorBackend:
    def begin(self, tab="\t"):
        self.code: list[string] = []
        self.tab = tab
        self.level = 0

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
    def __init__(self):
        self.backend: CodeGeneratorBackend = CodeGeneratorBackend()
        self.known_vars: list[str] = []
        self.known_mutexe: list[str] = []

    def create_main(self):
        self.backend.begin(tab="    ")
        self.backend.write('#!/usr/bin/python3\n')
        self.backend.write('\n')
        self.backend.write('import threading\n')
        self.backend.write('from threading import Thread\n')
        self.backend.write('\n')
        self.backend.write('def main():\n')
        self.backend.indent()
    def call_main(self):
        self.backend.dedent()
        self.backend.write('\n')
        self.backend.write('if __name__ == "__main__":\n')
        self.backend.indent()
        self.backend.write('main()\n')
    def create_thread(self, name: string, params: list[str]):
        self.backend.dedent()
        self.backend.write('\n')
        # print(params)
        self.backend.write('def {0}({1}):\n'.format(name, ", ".join(params)))
        self.backend.indent()

    def traverse_tree(self, root_call: bool, siccl_array: np.array, thread_dgraph: list[tuple[str, list[str]]], thread_mgraph: list[tuple[str, list[str]]], thread_pgraph: list[tuple[str, list[str]]]) -> None:
        inited_mutexe: list[str] = []
        last_thread_name = ""
        for i, elem in enumerate(siccl_array):
            mutex_name = elem[3]
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]

            # new thread
            if last_thread_name != thread_name:
                if root_call: 
                    self.create_main();
                    root_call = False
                else: 
                    thread_params: list[str] = []
                    for params_per_thread in thread_pgraph:
                        if params_per_thread[0] == thread_name:
                            thread_params = params_per_thread[1]
                    self.create_thread(thread_name, thread_params);


            if var_name not in self.known_vars:
                self.backend.write('{0} = [{1}, {2}]\n'.format(var_name, randint(0, 100), randint(0, 100)))
                self.known_vars.append(var_name)
            else:
                if mutex_name != "":
                    self.backend.write("{0}.acquire()\n".format(mutex_name))
                self.backend.write('{0}[0] = {1}\n'.format(var_name, randint(0, 100)))
                if mutex_name != "":
                    self.backend.write("{0}.release()\n".format(mutex_name))

            if i >= len(siccl_array)-1 or siccl_array[i+1][1] != thread_name:
                for deps_per_thread in thread_dgraph:
                    if deps_per_thread[0] == thread_name:
                        for dependant_thread in deps_per_thread[1]:
                            for mutexe_per_thread in thread_mgraph:                
                                if mutexe_per_thread[0] == dependant_thread:
                                    for next_thread_mutex in mutexe_per_thread[1]:
                                        if next_thread_mutex not in self.known_mutexe:
                                            self.backend.write("global {0}\n".format(next_thread_mutex))
                                            self.backend.write("{0} = threading.Lock()\n".format(next_thread_mutex))
                                            self.known_mutexe.append(next_thread_mutex)

                            thread_params: list[str] = []
                            for params_per_thread in thread_pgraph:
                                if params_per_thread[0] == dependant_thread:
                                    thread_params = params_per_thread[1]
                            self.backend.write('t_{0} = Thread(target={0}, args=({1},)) \n'.format(dependant_thread, ", ".join(thread_params)))
                            self.backend.write('t_{0}.start()\n'.format(dependant_thread))
            
            last_thread_name = thread_name
    def generate_thread_dependency_graph(self, siccl_array: np.array) -> list[tuple[str, list[str]]]:
        thread_dgraph: tuple[str, list[str]] = []

        last_thread_name = ""
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

            last_thread_name = thread_name[1]

        return thread_dgraph


    def get_threads_params(siccl_array: np.array, thread_name: str) -> list[str]:        
        res: list[str] = []
        for i, elem in enumerate(siccl_array):
            # print()
            if elem[1] == thread_name:
                if elem[2] not in res:
                    res.append(elem[2])
        return res

    def generate_thread_params_graph(self, siccl_array: np.array) -> list[tuple[str, list[str]]]:
        thread_pgraph: tuple[str, list[str]] = []
        last_thread_name = ""
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
                    dup_removed_params = params.copy()
                    for param in dup_removed_params:
                        if param in node[1]:
                            dup_removed_params.remove(param)
                    node[1].extend(dup_removed_params)

        return thread_pgraph

    def generate_thread_mutex_graph(self, siccl_array: np.array) -> list[tuple[str, list[str]]]:
        thread_mutex_graph: tuple[str, list[str]] = []

        for i, elem in enumerate(siccl_array):
            mutex_name = elem[3]
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]
            found = False

            for i, node in enumerate(thread_mutex_graph):
                if thread_name == node[0]:
                    found = True
                    if mutex_name not in node[1] and mutex_name != "":
                        node[1].append(mutex_name)
            if not found:
                thread_mutex_graph.append((thread_name, [mutex_name]))

        return thread_mutex_graph

    # probably one of the most inefficient thing I've ever written...
    def generate(self, siccl_array: list) -> string:
        # generating the graphs seperately is a (great)bit more inefficient but more readable
        thread_dgraph = self.generate_thread_dependency_graph(siccl_array)
        thread_mgraph = self.generate_thread_mutex_graph(siccl_array)
        thread_pgraph = self.generate_thread_params_graph(siccl_array)
        self.traverse_tree(True, siccl_array, thread_dgraph, thread_mgraph, thread_pgraph)
        self.call_main();
        return self.backend.end()
