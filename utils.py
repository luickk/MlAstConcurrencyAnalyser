from collections.abc import Iterable

def parse_var(var_name: str) -> tuple[str, any]:
    mutex_name = None
    split_res = var_name.split("_")
    if len(split_res) >= 2:
        if split_res[1][0] == "m":
            mutex_name = split_res[1]
        else:
            raise("SICCL syntax error: Mutex name has to start with an m")
    return (split_res[0], mutex_name)

# https://stackoverflow.com/questions/17864466/flatten-a-list-of-strings-and-lists-of-strings-and-lists-in-python
def flatten(input: list[str]) -> list[str]:
    res: list[str] = []
    for i in input:
        if isinstance(i, Iterable) and not isinstance(i, str):
            for subc in flatten(i):
                res.append(subc)
        else:
            res.append(i)
    return res

# very slow
def remove_dup(input: list[str]) -> list[str]:
    res: list[str] = []
    for elem in input:
       if elem not in res:
          res.append(elem)
    return res