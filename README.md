# Concurrency analasys based on Ml training with run/compile time data 

The basic idea is to train a ML model, in a unsupervised self-testing environment, advanced patterns of concurrency issues. The goal is to have it output a probability value for any given piece of SICCL(see below) code without being trained on a dataset.

Note: Throwing Ml against NP complete problems is nothing new, in this case it's especially difficult because tripping a certain kind of concurrency issues can take a long time, which is suboptimal for Ml training.

# Todo

- [x] Approximating feasibility of the project
	- Creating an abstract formal language describing different concurrency configurations(from which a python program is generated) seems to be possible
	- Building a graph from compile and runtime data is possible and has been done by thread/ mem sanitizers (as real model input samples)
- [x] Writing a simulation environment that generates a concurrent program from an SICCL like abstraction
- [ ] Putting it all together....


# Approach

## ML model

Since it's difficult to generate a dataset, a reinforcement learning approach is the most obvious to choose. The great problem is the generation of sample programs that are executable and *have a high enough entropy*.

Since generating python code is simply too complex for a simple reinforcement learning model I created SICCL(Simple Initial Concurrency Configuration Language -> see below), which acts as an abstraction layer to the reinforcement learning model. Since finding a proper policy function for a "language" is difficult, I will be using a [model free approach](https://en.wikipedia.org/wiki/Model-free_(reinforcement_learning)).

The basic values the model will optimise for are size (len of the SICCL script) and validity. Crashes or bad static scans (for example through valgrind) will result in bad scores...

## Code Generation

The GAN generates SICCL (see below) which is then turned into python code, run and tested on potential concurrency issues. Wether there was an issue and all kinds of runtime information is then passed to the GAN to optimise on.

### Simple Initial Concurrency Configuration Language (SICCL)

SICCL is a very rudamentary formal language describing intitial concurrent configurations of a program. 
The only entities are threads and variales. Every new dimension resembles a new thread. 
In the future the language could include gramar/ syntax for locking, syncing, timing delays to provide a reduced but complex enough environment for the model to experiment with.

For example:
```
{
	// main thread
	"var1_m1",
	"var2",
	"var3",
	{
		// thread 1 called by main
		"var1_m1"
	},
	{
		// thread 2 called by main
		"var1_m1",
		"var2",
		{
			// thread 3 called by thread2
			"var2",
			{
				// thread 4 called by thread3
				"var3",
				"var1_m1",
			}
		}
	},
	"var4",
	{
		"var4", 
		"var2"
	}
}
```
Syntax:
- Variables are string formatted like that: `<variable name>_<mutex name>`
- Threads: `{ <vars...> }` every new dimension is a thread

Prerequisite: 
- All variables used by a thread must be listed *before* the next thread!

## Fundamentals

It's difficult to find information on how modern thread sanitizers work and existing sanitizers are hidden in or built on top of big codebases which makes it difficult to learn from them. [This](https://static.googleusercontent.com/media/research.google.com/de//pubs/archive/35604.pdf) is a great paper on the fundemntals though.

## Tools for Instrumentation/ Interception, AST analysis

Since the approach of this project to generate a proper learning environment for the Ml model is a mix of run and compiletime data, both AST code and runtime information need to be combined into one graph.
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

