# Machine Learning based AST Concurrency Analyser

The basic idea is to train a ML model in a unsupervised self-testing environment advanced patterns of concurrency issues. The goal is to have it output a probability value for any given peace of AST code wihtout being trained on a dataset.

# Setup

## Installing LibClang bindings
- `pip3 install clang`
- Locate the libclang shared lib. On Mac: `mdfind -name libclang.dylib`
- Adjust `clang.cindex` (the python module) `set_library_path(path)` in the source code.

More info can be found [here](https://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang)