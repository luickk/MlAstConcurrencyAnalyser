import string
from random import randint
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

    def traverse_tree(self, root_call: bool, siccl_array: list, next_thread: (string, list)) -> None:
        future_threads_lookup: bool = False        
        future_threads: list[(string, list)] = []
        future_threads_i: int = 0
        for i, elem in enumerate(siccl_array):
            if isinstance(elem, list):
                if not future_threads_lookup:
                    future_threads_lookup = True
                    for new_threads in siccl_array[i:]:
                        if isinstance(new_threads, list):                        
                            for new_threads_vars in new_threads:
                                if isinstance(new_threads_vars, str):
                                    var_name = utils.parse_var(new_threads_vars)[0]
                                    mutex_name = utils.parse_var(new_threads_vars)[1]
                                    if mutex_name != None:
                                        if not mutex_name in self.known_mutexe:
                                            self.backend.write("global {0}\n".format(mutex_name))
                                            self.backend.write("{0} = threading.Lock()\n".format(mutex_name))
                                            self.known_mutexe.append(mutex_name)

                            new_thread_name = "thread_{0}".format(randint(0, 100))
                            # first flattening and then removing duplicates and correcting variable names
                            new_thread_params: list[str] = utils.flatten(new_threads)
                            for i, name in enumerate(new_thread_params): new_thread_params[i] = utils.parse_var(name)[0]
                            new_thread_params = utils.remove_dup(new_thread_params)
                            
                            self.backend.write('t_{0} = Thread(target={0}, args=({1},)) \n'.format(new_thread_name, ", ".join(new_thread_params)))
                            self.backend.write('t_{0}.start()\n'.format(new_thread_name))
                            future_threads.append((new_thread_name, new_thread_params))
                        else:
                            raise("SICCL syntax error: all vars have to be declared at the beginning")

                self.traverse_tree(False, elem, future_threads[future_threads_i])
                future_threads_i += 1
            else: 
                if i == 0:
                    if root_call: 
                        self.create_main();
                    else: 
                        self.create_thread(next_thread[0], next_thread[1]);

                var_name = utils.parse_var(elem)[0]                
                mutex_name = utils.parse_var(elem)[1]
                if var_name not in self.known_vars:
                    self.backend.write('{0} = [{1}, {2}]\n'.format(var_name, randint(0, 100), randint(0, 100)))
                    self.known_vars.append(var_name)
                else:
                    if mutex_name != None:
                        self.backend.write("{0}.acquire()\n".format(mutex_name))
                    self.backend.write('{0}[0] = {1}\n'.format(var_name, randint(0, 100)))
                    if mutex_name != None:
                        self.backend.write("{0}.release()\n".format(mutex_name))

    def generate(self, siccl_array: list) -> string:
        self.traverse_tree(True, siccl_array, ("", []))
        self.call_main();
        return self.backend.end()

if __name__ == "__main__":
    siccl_example = ["var1_m1", "var2", "var3", ["var1_m1"], ["var1_m1","var2", ["var2", ["var3","var1"]]], ["var3","var2"]]
    gen = SicclGenerator()
    text = gen.generate(siccl_example)
    
    f = open("final.py",'w')
    f.write(text)
    f.close()

    print(text)
    
