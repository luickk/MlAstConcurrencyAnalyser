# Concurrency analasys based on run/compile time data Ml training

The basic idea is to train a ML model, in a unsupervised self-testing environment, advanced patterns of concurrency issues. The goal is to have it output a probability value for any given piece of AST code(with runntime data) without being trained on a dataset.

Note: Throwing Ml against NP complete problems is nothing new, in this case it's especially difficult because tripping a certain kind of concurrency issues can take a long time, which is suboptimal for Ml training.

# Todo

- [x] Approximating feasibility of the project
	- Simulating different concurrency patterns (as model input) seems to be possible
	- Building an abstract graph from compile and runtime data is possible and has been done by thread/ mem sanitizers (as real model input samples)
	- Finding a fitting Ml model that can handle an unsupervised learning approach is also not an issue
- [ ] Generating graph from runtime interception/ memory instrumentation and AST data
- [ ] Writing a simulation environment that generates a concurrent program from an AST like abstraction
- [ ] Putting it all together....


# Approach

## ML model

Since it's difficult to generate a dataset, an unsupervised learning approach is the most obvious to choose. The great problem is the generation of sample programs that are executable and *have a high enough entropy*. I'm relatively sure that if the code generation is not integrated in the model, as for example in a [GAN](https://de.wikipedia.org/wiki/Generative_Adversarial_Networks), the entropy and as such the possibility for concurrency/ sync bugs would be far too low. Also, it would be vastly inefficient, opposing to an optimized generator/ discriminator model.

## Code Generation

As for now the plan is to create a parametrized abstraction of each program that consists of compile time AST(READS, WRITES, LOCKS, etc. on certain global or thread shared vars) analysis and runtime SIGNAL data (similar to the helgrind or llvm tsan, more [here](https://static.googleusercontent.com/media/research.google.com/de//pubs/archive/35604.pdf). That abstraction, together with the AST data(at least partially) is then fed to the ML model. 
Currently, the preferred Ml model is a [GAN](https://de.wikipedia.org/wiki/Generative_Adversarial_Networks) like one which has a generator that would generate the abstract compile time AST from which a program equivalent would then be statically generated to be fed back to the discriminator.

## Fundamentals

It's difficult to find information on how modern thread sanitizers work and existing sanitizers are hidden in or built on top of big codebases which makes it difficult to learn from them. [This](https://static.googleusercontent.com/media/research.google.com/de//pubs/archive/35604.pdf) is a great paper on the fundemntals though.

## Tools for Instrumentation/ Interception, AST analysis

Since the approach of this project to generate a proper dataset for the Ml model is a mix of run and compiletime data, both AST code and runtime information need to be combined into one graph.
For AST parsing and analysis, LLVM offers libclang which is really handy and covers all requirements. 

In order to generate a somewhat complete graph, we need the memory access information, which can only be read through memory instrumentation.
Intercepting function calls alone will not be enough but could have been easily achieved through [Clangs natively supported](https://maskray.me/blog/2023-01-08-all-about-sanitizer-interceptors) fn wrapper functionality. 

For memory instrumentation, there are multiple external tools available.
- QBDI is great but lacks support of multithreading(?)
- Frida is a really heavy framework that is not suited for fast program analysis evolutions as required for Ml training
- DynamoRIO requires a "runtime" or a binary that inserts the generated shared lib into the target process but supports multiple threads and enables somewhat(relatively speaking) lightweight memory instrumentation.

Since it took some time to find the right literature, here a few links:
- https://gcc.gnu.org/wiki/cauldron2012?action=AttachFile&do=get&target=kcc.pdf
- https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/data-race-test/ThreadSanitizerLLVM.pdf
- https://github.com/google/sanitizers/wiki/ThreadSanitizerAlgorithm
- https://storage.googleapis.com/pub-tools-public-publication-data/pdf/37278.pdf
- https://storage.googleapis.com/pub-tools-public-publication-data/pdf/35604.pdf
- https://github.com/google/sanitizers/wiki/ThreadSanitizerAlgorithm
- https://github.com/MattPD/cpplinks/blob/master/analysis.dynamic.md#software-sanitizers
- https://valgrind.org/docs/valgrind2007.pdf
- https://github.com/QBDI/QBDI


# Setup

## Installing LibClang bindings
- `pip3 install clang`
- Locate the libclang shared lib. On Mac: `mdfind -name libclang.dylib`
- Adjust `clang.cindex` (the python module) `set_library_path(path)` in the source code.

More info can be found [here](https://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang)


## Getting to run DynamoRIO
- Download the latest release from their Docs page
- There isn't too many requirements apart from making the project findable for CMake.
- Similar to Valgrind they have tools or clients that can be written with their C API.
- If the client (or tool) is built, it can be run with `DynamoRIO/bin64/drrun -c build/myClient.so -- anyExecutable`
- Technically it runs on MacOs, but there is no release built available, so I'm running it in an emulated Aarch64 Ubuntu.

