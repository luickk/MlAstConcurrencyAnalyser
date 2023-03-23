import string
from random import randint

class CodeGeneratorBackend:

    def begin(self, tab="\t"):
        self.code = []
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
        self.to_generate_threads: list
        self.to_generate_index: int

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
    def create_thread(self, name):
        self.backend.dedent()
        self.backend.write('\n')
        self.backend.write('def {0}():\n'.format(name))
        self.backend.indent()

    def generate(self, root_call: bool, siccl_array: list):
        for i, elem in enumerate(siccl_array):
            if isinstance(elem, list):
                self.generate(False, elem)
            else: 
                if i == 0:
                    if root_call: 
                        self.create_main();
                    else: 
                        print(self.to_generate_index, len(self.to_generate_threads))
                        self.create_thread(self.to_generate_threads[self.to_generate_index]);
                        self.to_generate_index += 1
                self.backend.write('{0} = {1}\n'.format(elem, randint(0, 100)))
                # print(i, elem)
                # check if this is the last variable
                if i < len(siccl_array)-1 and isinstance(siccl_array[i+1], list):
                    threads = len(siccl_array)- (i + 1)
                    self.to_generate_threads = []
                    self.to_generate_index = 0
                    for i in range(threads):
                        new_thread_name = "thread_{0}".format(randint(0, 100))
                        self.backend.write('t_{0} = Thread(target={0}, args=()) \n'.format(new_thread_name))
                        self.backend.write('t_{0}.start()\n'.format(new_thread_name))
                        self.to_generate_threads.append(new_thread_name)

if __name__ == "__main__":
    siccl_example = ["var1", "var2", "var3", ["var1"], ["var1","var2"]]
    p = SicclGenerator()
    p.generate(True, siccl_example)
    p.call_main();
    f = open("final.py",'w')
    f.write(p.backend.end())
    f.close()
    # print(siccl_example)
