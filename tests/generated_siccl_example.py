#!/usr/bin/python3

import threading
import time
from threading import Thread

exit_loops = False
end_loop_shared_vars_res: dict[int, list[int]] = {}
per_thread_loop_count = [0]*6

def end_loops_timer_thread():
    time.sleep(1)
    globals()["exit_loops"] = True
    time.sleep(0.5)
    shared_vars_count: dict[int, int] = {}
    thread_pgraph = {1: [0, 3, 7, 5, 1, 15, 16], 3: [0, 1], 4: [0], 5: [0]}

    for thread, params in thread_pgraph.items():
        for dgraph_var in params:
            if dgraph_var in shared_vars_count:
                shared_vars_count[dgraph_var] += per_thread_loop_count[thread]
            else:
                shared_vars_count[dgraph_var] = per_thread_loop_count[thread]
    print(end_loop_shared_vars_res)
    assert(len(shared_vars_count) == len(end_loop_shared_vars_res))
    for i, (key, val) in enumerate(end_loop_shared_vars_res.items()): 
        average = sum(val) / len(val)
        print(str(key) + ":" + str(shared_vars_count[key]-average))
    
    

def main():
    var_0 = [0, 0]
    var_3 = [0, 0]
    var_7 = [0, 0]
    var_0 = [0, 0]
    var_5 = [0, 0]
    var_1 = [0, 0]
    var_1 = [0, 0]
    var_15 = [0, 0]
    var_16 = [0, 0]
    arguments = locals()
    loop_stop_thread = Thread(target=end_loops_timer_thread, args=()) 
    loop_stop_thread.start()
    global mutex_2
    mutex_2 = threading.Lock()
    var_0 = [0, 0]
    var_1 = [0, 0]
    t_3 = Thread(target=thread_3, args=(var_0, var_1,)) 
    t_3.start()
    while not exit_loops:
        per_thread_loop_count[1] += 1
        var_0[0] += 1
        var_0[0] += 1
        var_1[0] += 1
        mutex_2.acquire()
        var_1[0] += 1
        mutex_2.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_3(var_0, var_1):
    arguments = locals()
    global mutex_1
    mutex_1 = threading.Lock()
    t_4 = Thread(target=thread_4, args=(var_0,)) 
    t_4.start()
    t_5 = Thread(target=thread_5, args=(var_0,)) 
    t_5.start()
    while not exit_loops:
        per_thread_loop_count[3] += 1
        var_0[0] += 1
        var_0[0] += 1
        mutex_2.acquire()
        var_1[0] += 1
        mutex_2.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_4(var_0):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[4] += 1
        mutex_1.acquire()
        var_0[0] += 1
        mutex_1.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_5(var_0):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[5] += 1
        mutex_1.acquire()
        var_0[0] += 1
        mutex_1.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

if __name__ == "__main__":
    main()
