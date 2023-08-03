from collections.abc import Iterable
import io

def parse_var(var_name: str) -> tuple[str, any]:
    mutex_name = None
    split_res = var_name.split("_")
    if len(split_res) >= 2:
        if split_res[1] != None:
            mutex_name = split_res[1]
    return (split_res[0], mutex_name)

# https://stackoverflow.com/questions/17864466/flatten-a-list-of-strings-and-lists-of-strings-and-lists-in-python
def flatten(input: list[str]) -> list[str]:
    res: list[str] = []
    for i in input:
        if isinstance(i, Iterable) and not isinstance(i, str) and not isinstance(i, int):
            for subc in flatten(i):
                res.append(subc)
        else:
            res.append(i)
    return res

# very slow
def remove_dup(input: list[int]) -> list[int]:
    res: list[int] = []
    for elem in input:
       if elem not in res:
          res.append(elem)
    return res


# very slow
def count_unique(input: list[int]) -> int:
    res: list[int] = []
    n_unique = 0
    for elem in input:
       if elem not in res:
          n_unique += 1
          res.append(elem)
    return n_unique

def index_multi_dim_multi_axis_list(to_scan_list: list, index: list, value_to_set = None) -> any:
    next_dim_list = to_scan_list
    for elem in index:
        if elem >= len(next_dim_list):
            return None
        if isinstance(next_dim_list[elem], list):
            next_dim_list = next_dim_list[elem]
        else:
            if value_to_set != None:
                next_dim_list[elem] = value_to_set
                return
            else:
                return next_dim_list[elem]


def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

def map_value(in_v, in_min, in_max, out_min, out_max):
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if v < out_min: 
        v = out_min 
    elif v > out_max: 
        v = out_max
    return v