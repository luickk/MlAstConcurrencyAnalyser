#!/usr/bin/python3

import threading
import time
from threading import Thread

exit_loops = False
end_loop_shared_vars_res: list[int, list[int]] = []
per_thread_loop_count = [0]*8

def end_loops_timer_thread():
    time.sleep(1)
    globals()["exit_loops"] = True
    time.sleep(0.5)
    shared_vars_count: list[int, int] = []
    thread_pgraph = [(1, [2, 3]), (5, [2, 3]), (6, [2, 3]), (7, [2])]

    for i_thread, thread in enumerate(thread_pgraph):
        for dgraph_var in thread[1]:
            found = False
            for var_count in shared_vars_count:
                if dgraph_var == var_count[0]:
                    found = True
                    var_count[1] += per_thread_loop_count[thread[0]]
            if not found:
                shared_vars_count.append([dgraph_var, per_thread_loop_count[thread[0]]])
    assert(len(shared_vars_count) == len(end_loop_shared_vars_res))
    for i, var in enumerate(end_loop_shared_vars_res): 
        average = sum(var[1]) / len(var[1])
        print(str(var[0]) + ":" + str(shared_vars_count[i][1]-average))
    
    

def main():
    arguments = locals()
    loop_stop_thread = Thread(target=end_loops_timer_thread, args=()) 
    loop_stop_thread.start()
    global mutex_2
    mutex_2 = threading.Lock()
    global mutex_3
    mutex_3 = threading.Lock()
    var_2 = [71, 63]
    var_3 = [7, 68]
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
        found = False
        for elem in end_loop_shared_vars_res:
            if elem[0] == param:
                found = True
                elem[1].append(arguments["var_" + str(param)][0])
        if not found:
            end_loop_shared_vars_res.append([param, [arguments["var_" + str(param)][0]]])

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
        found = False
        for elem in end_loop_shared_vars_res:
            if elem[0] == param:
                found = True
                elem[1].append(arguments["var_" + str(param)][0])
        if not found:
            end_loop_shared_vars_res.append([param, [arguments["var_" + str(param)][0]]])

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
        found = False
        for elem in end_loop_shared_vars_res:
            if elem[0] == param:
                found = True
                elem[1].append(arguments["var_" + str(param)][0])
        if not found:
            end_loop_shared_vars_res.append([param, [arguments["var_" + str(param)][0]]])

def thread_7(var_2):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[7] += 1
        mutex_2.acquire()
        var_2[0] += 1
        mutex_2.release()

if __name__ == "__main__":
    main()
