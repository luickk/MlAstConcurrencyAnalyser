import ast
import astunparse

class GenericVisitor(ast.NodeVisitor):

    def __init__(self):
        self.last_declared_fn = ""
        self.vars_fns = []
        self.fn_fns = []
        self.mutex_state = {}
        self.mutex_counter = 0

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
            # print("funcname", func_name)
            if isinstance(node.func.value, ast.Name):
                func_attr = node.func.value.id
                mutex_id = 0
                state = 0
                if func_name == "acquire" or func_name == "release":
                    if func_name == "acquire": state = 1
                    if func_attr in self.mutex_state:
                        self.mutex_state[func_attr] = state
                    else:
                        mutex_id = self.mutex_counter
                        self.mutex_state[func_attr] = state
                        self.mutex_counter += 1
                    
        # print(self.mutex_state)
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                fn_name = node.value.func.id
                if fn_name == "Thread":
                    fn_arg = node.value.keywords[0].value.id
                    if len(self.fn_fns) <= 0:
                        self.fn_fns.append(("", self.last_declared_fn))
                    self.fn_fns.append((self.last_declared_fn, fn_arg))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.last_declared_fn = node.name
        self.generic_visit(node)

    def visit_Name(self, node):
        # print("Variable name:", node.id)
        if node.id in self.mutex_state:
            mutex_state = self.mutex_state[node.id]
        else:
            mutex_state = None
        mutex_id = 0
        if mutex_state == 1:
            mutex_id = node.id
        self.vars_fns.append((self.last_declared_fn, node.id, mutex_id))


def generate_siccle_arr(vars_fns, fn_fns):
    print(fn_fns)
    fn_counter = 0
    var_counter = 0
    mutex_counter = 0
    known_fn = {}
    known_mutexe = {}
    known_vars = {}

    siccl_array_tok = []
    for i_fns, fn in enumerate(fn_fns):
        calling_fn_id = 0
        if fn[0] in known_fn:
            calling_fn_id = known_fn[fn[0]]
        else:
            calling_fn_id = fn_counter
            known_fn[fn[0]] = fn_counter
            fn_counter += 1

        called_fn_id = 0
        if fn[1] in known_fn:
            called_fn_id = known_fn[fn[1]]
        else:
            called_fn_id = fn_counter
            known_fn[fn[1]] = fn_counter
            fn_counter += 1

        var_id = 0
        mutex_id = 0
        for var in vars_fns:
            if var[0] == fn[1]:
                if var[1] in known_vars:
                    var_id = known_vars[var[1]]
                else:
                    var_id = var_counter
                    known_vars[var[1]] = var_counter
                    var_counter += 1

                if var[2] in known_mutexe:
                    mutex_id = known_mutexe[var[2]]
                else:
                    mutex_id = mutex_counter
                    known_mutexe[var[2]] = mutex_counter
                    mutex_counter += 1
                
                siccl_array_tok.append([calling_fn_id, called_fn_id, var_id, mutex_id])
    return siccl_array_tok