from collections.abc import Iterable

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