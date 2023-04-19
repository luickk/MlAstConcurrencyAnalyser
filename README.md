# Concurrency analysis based on Ml training with run/compile time data 

The basic idea is to train a ML model, in an unsupervised self-testing environment, advanced patterns of concurrency issues. The goal is to have it output a probability value for any given piece of SICCL(see below) code without being trained on a dataset.

Note: Throwing Ml against NP complete problems is nothing new, in this case it's especially difficult because tripping a certain kind of concurrency issues can take a long time, which is suboptimal for Ml training.

# Todo

- [x] Approximating feasibility of the project
    - Creating an abstract formal language describing different concurrency configurations(from which a python program is generated) seems to be possible
    - Building a graph from compile and runtime data is possible and has been done by thread/ mem sanitizers (as real model input samples)
- [x] Writing a simulation environment that generates a concurrent program from an SICCL like abstraction
- [x] Putting it all together....

## Log Book

### First working version (commit: )

This commit contains the first working version of the project. The network manages to assign new variables the same mutexe over different threads. Although being a very(very) simple task to accomplish, the little time it took the network to get there makes me very optimistic that when scaling the complexity and context information, the network will be able to keep up.

Initial SICCL matrix:

```
# parent arr, thread name, var name, mutex name
siccl_example_flattened = np.array([[0, 1, 2, 0],
                                    [0, 1, 3, 0],
                                    [1, 5, 2, 0], 
                                    [1, 5, 3, 0], 
                                    [5, 6, 2, 0], 
                                    [5, 6, 3, 0], 
                                    [5, 7, 2, 0]], dtype=int)
```

After 10 iterations:

```
[[0 1 2 0]
 [0 1 3 9]
 [1 5 2 0]
 [1 5 3 1]
 [5 6 2 1]
 [5 6 3 1]
 [5 7 2 0]]
```
Missing non atomic operations:  
3: 1567951.0
3: 259231.5
Reward: 0.695464946900354
Loss: -3


After 200 iterations
```
[[0 1 2 0]
 [0 1 3 1]
 [1 5 2 0]
 [1 5 3 1]
 [5 6 2 1]
 [5 6 3 1]
 [5 7 2 0]]
2: 250748.0
3:  0.5
```
Missing non atomic operations:  
- 250748.0
- 0.5
Reward: 0.9582021953186979
Loss: 1

# Approach

## ML model

Since it's difficult to generate a dataset, a reinforcement learning approach is the most obvious to choose. The great problem is the generation of sample programs that are executable and *have a high enough entropy*.

Since generating python code is simply too complex for a simple reinforcement learning model, I created SICCL(Simple Initial Concurrency Configuration Language -> see below), which acts as an abstraction layer to the reinforcement learning model. Since finding a proper policy function for a "language" is difficult, I will be using a [model free approach](https://en.wikipedia.org/wiki/Model-free_(reinforcement_learning)).

The basic values the model will optimize for are size (len of the SICCL script) and validity. Crashes or bad static scans (for example through valgrind) will result in bad scores...

## Code Generation

The GAN generates SICCL (see below) which is then turned into python code, run and tested on potential concurrency issues. Whether there was an issue and all kinds of runtime information is then passed to the GAN to optimize on.

## Concurrency issue detection

Concurrency issue detection can be a very complex endeavor but since we don't need a high degree of abstraction or readability but really only some indication value we will keep it simple. In python, not all operations on lists are atomic so that they just miss in the end result. That is quite useful if you know what they should be. So the concurrency issue indicator will be a function of how many non atomic operations on a list have not been "executed" (e.g. are missing) compared to how many should have been "executed, the delta is the indicator.

The from the SICCL script generated python script includes the calculation of the indicator(the delta of all threads(loops) in which the variable is increased by one, and the actual value of the variable).
If there is not enough mutexe, the add operation might not be applied on the variable, which does not get increased as a result. The greater the difference of the value, the variable should have had(the sum of all the loops it's referenced in) and the actual value, the more collisions were happening.
That does not compensate for potential data races, but that can be added later.

### Detection results

This very simple indicator works great with a very low error rate compared to its delta of mutex vs no mutex usage.

- Results with 2 variables, 4 threads, with 2(different) mutexe and 1 sec runtime:
    Script:
    ```python
    #   parent arr, thread id, var id, mutex id
    siccl_example_flattened = np.array([[0, 1, 2, 2],
                                        [0, 1, 3, 3],
                                        [1, 5, 2, 2], 
                                        [1, 5, 3, 3], 
                                        [5, 6, 2, 2], 
                                        [5, 6, 3, 3], 
                                        [5, 7, 2, 2]], dtype=int) 
    ```
    Results:
    ```
    var 2 diff:  -57
    var 3 diff:  -32
    ```
    A negative difference should theoretically not be possible, since it would indicate that there have been more iterations applied on a variable than there actually were. That's the error, which is somewhere in the lower second digits, which is negligible compared to the non-atomic addition operation misses if there are no mutexe.

- Results with 2 variables, 4 threads, *0* mutexe and 1 sec runtime:
    Script:
    ```python
    #   parent arr, thread id, var id, mutex id
    siccl_example_flattened = np.array([[0, 1, 2, 0],
                                        [0, 1, 3, 0],
                                        [1, 5, 2, 0], 
                                        [1, 5, 3, 0], 
                                        [5, 6, 2, 0], 
                                        [5, 6, 3, 0], 
                                        [5, 7, 2, 0]], dtype=int) 
    ```
    Results:
    ```
    var 2 diff:  3604555
    var 3 diff:  1838930
    ```
    As we can see, without any mutexe, the amount of missed non-atomic addition operation increases drastically per variable.

### Simple Initial Concurrency Configuration Language (SICCL)

SICCL is a very rudimentary formal language describing initial concurrent configurations of a program. 
The only entities are threads and variables. Every new dimension resembles a new thread. 
In the future the language could include grammar/ syntax for locking, syncing, timing delays to provide a reduced but complex enough environment for the model to experiment with.

Originally I wanted to go with a multidimensional tree like structure where every new axis was a new thread. That was a lot more elegant, not just for readability, but also for generation. The problem was that numpy/ tensorflow doesn't really support multi axis arrays with different sizes, and transforming (mostly padding) them is more complex than just going with an already flattened(static in size and axes) structure. The new flattened version has the problem that thread information needs to be encoded as well.
For example:
```python
# thread id, var id, mutex id
[0, 1, 2, 4],
[0, 1, 3, 4],
[1, 5, 2, 4], 
[1, 5, 3, 0], 
[5, 6, 2, 4], 
[5, 6, 2, 4], 
[5, 7, 2, 4]
```
compiles to:

```python
#!/usr/bin/python3

import threading
import time
from threading import Thread

exit_loops = False

def end_loops_timer_thread():
    time.sleep(5)
    globals()["exit_loops"] = True

def main():
    loop_stop_thread = Thread(target=end_loops_timer_thread, args=()) 
    loop_stop_thread.start()
    var_2 = [92, 87]
    var_3 = [28, 27]
    t_5 = Thread(target=thread_5, args=(var_2, var_3,)) 
    t_5.start()
    while not exit_loops:
        var_2[0] = 47
        var_3[0] = 88

def thread_5(var_2, var_3):
    t_6 = Thread(target=thread_6, args=(var_2,)) 
    t_6.start()
    t_7 = Thread(target=thread_7, args=(var_2,)) 
    t_7.start()
    while not exit_loops:
        var_2[0] = 45
        var_3[0] = 10

def thread_6(var_2):
    while not exit_loops:
        var_2[0] = 100
        var_2[0] = 12

def thread_7(var_2):
    while not exit_loops:
        var_2[0] = 87

if __name__ == "__main__":
    main()

```
## Fundamentals

It's difficult to find information on how modern thread sanitizers work and existing sanitizers are hidden in or built on top of big codebases which makes it difficult to learn from them. [This](https://static.googleusercontent.com/media/research.google.com/de//pubs/archive/35604.pdf) is a great paper on the fundamentals though.

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

