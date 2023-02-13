# Machine Learning based AST Concurrency Analyser

The basic idea is to train a ML model in a unsupervised self-testing environment advanced patterns of concurrency issues. The goal is to have it output a probability value for any given peace of AST code wihtout being trained on a dataset.

# Approach

## ML model

Since it's difficult to generate a dataset, an unsupervised learning approach is the most obvious to choose. The great problem is the generation of sample programs that are executable and *have a high enough entropy*. I'm relatively sure that if the code generation is not integrated in the model, as for example in a [GAN](https://de.wikipedia.org/wiki/Generative_Adversarial_Networks), the entropy and as such the possibility for concurrency/ sync bugs would be far too low. Also, it would be vastly inefficient opposing to an optimized generator/ discriminator model.

## Code Generation

As for now the plan is to create a parametrized abstraction of each program that consists of compile time AST(READS, WRITES, LOCKS, etc. on certain global or thread shared vars) analysis and runtime SIGNAL data (similar to the helgrind or llvm tsan, more [here](https://static.googleusercontent.com/media/research.google.com/de//pubs/archive/35604.pdf). That abstraction, together with the AST data(at least partially) is then fed to the ML model. 
Currently the preferred Ml model is a [GAN](https://de.wikipedia.org/wiki/Generative_Adversarial_Networks) like one which has a generator that would generate the abstract compile time AST from which a program equivalent would then be statically generated to be fed back to the discriminator.

## Fundamentals

It's difficult to find information on how modern thread sanitizers work and existing sanitizers are hidden and built on top of big codebases which makes it difficult to learn from them. [This](https://static.googleusercontent.com/media/research.google.com/de//pubs/archive/35604.pdf) is a great paper on the fundemntals though.
And [this](https://maskray.me/blog/2023-01-08-all-about-sanitizer-interceptors) is a really helpful blogpost on how function interception in sanatizers work.

Since it took some time to find the right literature, here a few links:
- https://gcc.gnu.org/wiki/cauldron2012?action=AttachFile&do=get&target=kcc.pdf
- https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/data-race-test/ThreadSanitizerLLVM.pdf
- https://static.googleusercontent.com/media/research.google.com/ja//pubs/archive/35604.pdf
- https://github.com/google/sanitizers/wiki/ThreadSanitizerAlgorithm
- https://storage.googleapis.com/pub-tools-public-publication-data/pdf/37278.pdf
- https://storage.googleapis.com/pub-tools-public-publication-data/pdf/35604.pdf
- https://github.com/google/sanitizers/wiki/ThreadSanitizerAlgorithm
- https://github.com/MattPD/cpplinks/blob/master/analysis.dynamic.md#software-sanitizers

# Setup

## Installing LibClang bindings
- `pip3 install clang`
- Locate the libclang shared lib. On Mac: `mdfind -name libclang.dylib`
- Adjust `clang.cindex` (the python module) `set_library_path(path)` in the source code.

More info can be found [here](https://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang)