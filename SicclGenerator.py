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
        self.to_generate_threads: list[str] = []
        self.to_generate_threads_i: list[str] = []
        self.known_vars: list[str] = []

    def create_main(self):
        self.backend.begin(tab="    ")
        self.backend.write('#!/usr/bin/python3\n')
        self.backend.write('\n')
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
                print("traversing on instance")
                if not future_threads_lookup:
                    future_threads_lookup = True
                    for elem_elem in siccl_array[i:]:
                        if isinstance(elem_elem, list):
                            new_thread_name = "thread_{0}".format(randint(0, 100))
                            # first flattening and then removing duplicates
                            print(elem)
                            new_thread_params: list[str] = utils.remove_dup(utils.flatten(elem_elem))
                            print(new_thread_params)
                            self.backend.write('t_{0} = Thread(target={0}, args=({1},)) \n'.format(new_thread_name, ", ".join(new_thread_params)))
                            self.backend.write('t_{0}.start()\n'.format(new_thread_name))
                            future_threads.append((new_thread_name, new_thread_params))

                self.traverse_tree(False, elem, future_threads[future_threads_i])
                future_threads_i += 1
            else: 
                print("traversing on var")
                if i == 0:
                    if root_call: 
                        self.create_main();
                    else: 
                        self.create_thread(next_thread[0], next_thread[1]);
                if elem not in self.known_vars:
                    self.backend.write('{0} = [{1}, {2}]\n'.format(elem, randint(0, 100), randint(0, 100)))
                    self.known_vars.append(elem)
                else:
                    self.backend.write('{0}[0] = {1}\n'.format(elem, randint(0, 100)))
        print("done!")

    def generate(self, siccl_array: list) -> string:
        self.traverse_tree(True, siccl_array, ("", []))
        self.call_main();
        return self.backend.end()

if __name__ == "__main__":
    siccl_example = ["var1", "var2", "var3", ["var1"], ["var1","var2", ["var2", ["var3","var1"]]], ["var3","var2"]]
    gen = SicclGenerator()
    text = gen.generate(siccl_example)
    
    f = open("final.py",'w')
    f.write(text)
    f.close()

    print(text)
    
