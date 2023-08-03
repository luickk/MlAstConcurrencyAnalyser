#!/usr/bin/python3

import threading
import time
from threading import Thread

exit_loops = False
end_loop_shared_vars_res: dict[int, list[int]] = {}
per_thread_loop_count = [0]*8

def end_loops_timer_thread():
    time.sleep(1)
    globals()["exit_loops"] = True
    time.sleep(0.5)
    shared_vars_count: dict[int, int] = {}
    thread_pgraph = {0: [], 1: [2, 3], 5: [2, 3], 6: [2, 3], 7: [2]}

    for thread, params in thread_pgraph.items():
        for dgraph_var in params:
            if dgraph_var in shared_vars_count:
                shared_vars_count[dgraph_var] += per_thread_loop_count[thread]
            else:
                shared_vars_count[dgraph_var] = per_thread_loop_count[thread]
    for i, (key, val) in enumerate(end_loop_shared_vars_res.items()): 
        if key in shared_vars_count:
            average = sum(val) / len(val)
            print(str(key) + ":" + str(shared_vars_count[key]-average))
    
    

def main():
    var_2 = [0, 0]
    var_3 = [0, 0]
    arguments = locals()
    loop_stop_thread = Thread(target=end_loops_timer_thread, args=()) 
    loop_stop_thread.start()
    global mutex_2
    mutex_2 = threading.Lock()
    global mutex_3
    mutex_3 = threading.Lock()
    var_2 = [0, 0]
    var_3 = [0, 0]
    t_5 = Thread(target=thread_5, args=(var_2, var_3,)) 
    t_5.start()
    while not exit_loops:
        per_thread_loop_count[1] += 1
        mutex_2.acquire()
        var_2[0] += 1
        mutex_2.release()
        mutex_3.acquire()
        var_3[0] += 1
        mutex_3.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_5(var_2, var_3):
    arguments = locals()
    t_6 = Thread(target=thread_6, args=(var_2, var_3,)) 
    t_6.start()
    t_7 = Thread(target=thread_7, args=(var_2,)) 
    t_7.start()
    while not exit_loops:
        per_thread_loop_count[5] += 1
        mutex_2.acquire()
        var_2[0] += 1
        mutex_2.release()
        mutex_3.acquire()
        var_3[0] += 1
        mutex_3.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_6(var_2, var_3):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[6] += 1
        mutex_2.acquire()
        var_2[0] += 1
        mutex_2.release()
        mutex_3.acquire()
        var_3[0] += 1
        mutex_3.release()
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        if arguments["var_" + str(param)][0] != 0: 
            if param in end_loop_shared_vars_res:
                end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
            else:
                end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_7(var_2):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[7] += 1
        mutex_2.acquire()
        var_2[0] += 1
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

if __name__ == "__main__":
    main()
