from random import randint
import numpy as np
import string
import utils

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
        self.backend.write('def {0}({1}):\n'.format(name, ", ".join(params)))
        self.backend.indent()

    def traverse_tree(self, root_call: bool, siccl_array: np.array, next_thread: (string, list)) -> None:
        future_threads_lookup: bool = False        
        future_threads: list[(string, list)] = []
        future_threads_i: int = 0
        last_thread_name = ""
        for i, elem in np.ndenumerate(siccl_array):
            mutex_name = elem[3]
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]
            # new thread
            if last_thread_name == thread_name:
                if not mutex_name in self.known_mutexe:
                    self.backend.write("global {0}\n".format(mutex_name))
                    self.backend.write("{0} = threading.Lock()\n".format(mutex_name))
                    self.known_mutexe.append(mutex_name)

                index = thread_tree.index(thread_name)
                for elem_el in thread_tree[index]:
                    new_thread_name = elem_el[0]
                    new_thread_params = elem_el[1]

                    self.backend.write('t_{0} = Thread(target={0}, args=({1},)) \n'.format(thread_name, ", ".join(new_thread_params)))
                    self.backend.write('t_{0}.start()\n'.format(new_thread_name))
                    future_threads.append((new_thread_name, new_thread_params))
                
                self.traverse_tree(False, elem, future_threads[future_threads_i])
                future_threads_i += 1
            else: 
                if i == 0:
                    if root_call: 
                        self.create_main();
                    else: 
                        self.create_thread(next_thread[0], next_thread[1]);

                if var_name not in self.known_vars:
                    self.backend.write('{0} = [{1}, {2}]\n'.format(var_name, randint(0, 100), randint(0, 100)))
                    self.known_vars.append(var_name)
                else:
                    if mutex_name != None:
                        self.backend.write("{0}.acquire()\n".format(mutex_name))
                    self.backend.write('{0}[0] = {1}\n'.format(var_name, randint(0, 100)))
                    if mutex_name != None:
                        self.backend.write("{0}.release()\n".format(mutex_name))
    
    def generate_thread_graph(self, siccl_array: np.array) -> list[tuple[str, list[str]]]:
        thread_graph = []

        last_thread_name = ""
        for i, elem in enumerate(siccl_array):
            var_name = elem[2]
            thread_name = elem[1]
            parent_thread = elem[0]

            if last_thread_name != thread_name:
                i = 0
                found = False
                for i, node in enumerate(thread_graph):
                    if node[0] == thread_name:
                        found = True
                        if parent_thread not in node[1]:
                            node[1].append(parent_thread)
                if not found:
                    thread_graph.append((thread_name, [parent_thread]))

            last_thread_name = thread_name[1]
        return thread_graph

    def generate(self, siccl_array: list) -> string:
        thread_graph = self.generate_thread_graph(siccl_array)
        print(thread_graph)
        self.traverse_tree(True, siccl_array, ("", []))
        self.call_main();
        return self.backend.end()
