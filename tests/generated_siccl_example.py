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
    thread_pgraph = {1: [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 36, 38], 2: [25, 27, 18, 29, 30, 15, 31, 13, 32, 23, 19, 16, 17, 21, 33, 24], 3: [0, 1, 36, 3, 8, 9, 38, 12, 13, 5, 7, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 41], 4: [0, 1, 12, 13, 5, 8, 7, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], 5: [0, 1, 12, 13, 5, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 41]}

    for thread, params in thread_pgraph.items():
        for dgraph_var in params:
            if dgraph_var in shared_vars_count:
                shared_vars_count[dgraph_var] += per_thread_loop_count[thread]
            else:
                shared_vars_count[dgraph_var] = per_thread_loop_count[thread]
    assert(len(shared_vars_count) == len(end_loop_shared_vars_res))
    for i, (key, val) in enumerate(end_loop_shared_vars_res.items()): 
        average = sum(val) / len(val)
        print(str(key) + ":" + str(shared_vars_count[key]-average))
    
    

def main():
    var_0 = [0, 0]
    var_1 = [0, 0]
    var_2 = [0, 0]
    var_3 = [0, 0]
    var_2 = [0, 0]
    var_5 = [0, 0]
    var_6 = [0, 0]
    var_7 = [0, 0]
    var_6 = [0, 0]
    var_8 = [0, 0]
    var_9 = [0, 0]
    var_10 = [0, 0]
    var_3 = [0, 0]
    var_8 = [0, 0]
    var_9 = [0, 0]
    var_10 = [0, 0]
    var_12 = [0, 0]
    var_13 = [0, 0]
    var_5 = [0, 0]
    var_8 = [0, 0]
    var_5 = [0, 0]
    var_7 = [0, 0]
    var_9 = [0, 0]
    var_7 = [0, 0]
    var_14 = [0, 0]
    var_0 = [0, 0]
    var_15 = [0, 0]
    var_16 = [0, 0]
    var_17 = [0, 0]
    var_14 = [0, 0]
    var_15 = [0, 0]
    var_18 = [0, 0]
    var_16 = [0, 0]
    var_19 = [0, 0]
    var_20 = [0, 0]
    var_21 = [0, 0]
    var_15 = [0, 0]
    var_22 = [0, 0]
    var_20 = [0, 0]
    var_23 = [0, 0]
    var_23 = [0, 0]
    var_20 = [0, 0]
    var_0 = [0, 0]
    var_24 = [0, 0]
    var_20 = [0, 0]
    var_23 = [0, 0]
    var_20 = [0, 0]
    var_0 = [0, 0]
    var_24 = [0, 0]
    var_20 = [0, 0]
    arguments = locals()
    loop_stop_thread = Thread(target=end_loops_timer_thread, args=()) 
    loop_stop_thread.start()
    var_25 = [0, 0]
    var_27 = [0, 0]
    var_18 = [0, 0]
    var_29 = [0, 0]
    var_30 = [0, 0]
    var_15 = [0, 0]
    var_31 = [0, 0]
    var_13 = [0, 0]
    var_32 = [0, 0]
    var_23 = [0, 0]
    var_19 = [0, 0]
    var_16 = [0, 0]
    var_17 = [0, 0]
    var_21 = [0, 0]
    var_33 = [0, 0]
    var_24 = [0, 0]
    t_2 = Thread(target=thread_2, args=(var_25, var_27, var_18, var_29, var_30, var_15, var_31, var_13, var_32, var_23, var_19, var_16, var_17, var_21, var_33, var_24,)) 
    t_2.start()
    global mutex_1
    mutex_1 = threading.Lock()
    global mutex_2
    mutex_2 = threading.Lock()
    var_0 = [0, 0]
    var_1 = [0, 0]
    var_36 = [0, 0]
    var_3 = [0, 0]
    var_8 = [0, 0]
    var_9 = [0, 0]
    var_38 = [0, 0]
    var_12 = [0, 0]
    var_5 = [0, 0]
    var_7 = [0, 0]
    var_14 = [0, 0]
    var_20 = [0, 0]
    var_22 = [0, 0]
    var_41 = [0, 0]
    t_3 = Thread(target=thread_3, args=(var_0, var_1, var_36, var_3, var_8, var_9, var_38, var_12, var_13, var_5, var_7, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_41,)) 
    t_3.start()
    while not exit_loops:
        per_thread_loop_count[1] += 1
        var_0[0] += 1
        var_1[0] += 1
        var_3[0] += 1
        var_5[0] += 1
        var_7[0] += 1
        var_8[0] += 1
        var_9[0] += 1
        var_3[0] += 1
        var_8[0] += 1
        var_9[0] += 1
        var_12[0] += 1
        var_13[0] += 1
        mutex_1.acquire()
        var_5[0] += 1
        mutex_1.release()
        var_8[0] += 1
        var_5[0] += 1
        mutex_2.acquire()
        var_7[0] += 1
        mutex_2.release()
        var_9[0] += 1
        var_7[0] += 1
        var_14[0] += 1
        var_0[0] += 1
        var_15[0] += 1
        var_16[0] += 1
        var_17[0] += 1
        var_14[0] += 1
        var_15[0] += 1
        var_18[0] += 1
        var_16[0] += 1
        var_19[0] += 1
        var_20[0] += 1
        var_21[0] += 1
        var_15[0] += 1
        var_22[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        found = False
        if param in end_loop_shared_vars_res:
            end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
        else:
            end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_2(var_25, var_27, var_18, var_29, var_30, var_15, var_31, var_13, var_32, var_23, var_19, var_16, var_17, var_21, var_33, var_24):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[2] += 1
        var_25[0] += 1
        var_25[0] += 1
        var_27[0] += 1
        var_18[0] += 1
        var_18[0] += 1
        var_29[0] += 1
        var_30[0] += 1
        var_15[0] += 1
        var_29[0] += 1
        var_31[0] += 1
        var_15[0] += 1
        var_31[0] += 1
        var_27[0] += 1
        var_27[0] += 1
        var_31[0] += 1
        var_13[0] += 1
        var_30[0] += 1
        var_27[0] += 1
        var_31[0] += 1
        var_13[0] += 1
        var_30[0] += 1
        var_32[0] += 1
        var_27[0] += 1
        var_32[0] += 1
        var_23[0] += 1
        var_19[0] += 1
        var_16[0] += 1
        var_17[0] += 1
        var_21[0] += 1
        var_23[0] += 1
        var_33[0] += 1
        var_17[0] += 1
        var_32[0] += 1
        var_17[0] += 1
        var_24[0] += 1
        var_16[0] += 1
        var_24[0] += 1
        var_27[0] += 1
        var_16[0] += 1
        var_33[0] += 1
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        found = False
        if param in end_loop_shared_vars_res:
            end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
        else:
            end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_3(var_0, var_1, var_36, var_3, var_8, var_9, var_38, var_12, var_13, var_5, var_7, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_41):
    arguments = locals()
    t_4 = Thread(target=thread_4, args=(var_0, var_1, var_12, var_13, var_5, var_8, var_7, var_9, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24,)) 
    t_4.start()
    t_5 = Thread(target=thread_5, args=(var_0, var_1, var_12, var_13, var_5, var_8, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_41,)) 
    t_5.start()
    while not exit_loops:
        per_thread_loop_count[3] += 1
        var_0[0] += 1
        var_1[0] += 1
        var_36[0] += 1
        var_3[0] += 1
        var_8[0] += 1
        var_9[0] += 1
        var_36[0] += 1
        var_38[0] += 1
        var_3[0] += 1
        var_8[0] += 1
        var_38[0] += 1
        var_12[0] += 1
        var_13[0] += 1
        mutex_1.acquire()
        var_5[0] += 1
        mutex_1.release()
        var_8[0] += 1
        var_5[0] += 1
        mutex_2.acquire()
        var_7[0] += 1
        mutex_2.release()
        var_9[0] += 1
        var_7[0] += 1
        var_14[0] += 1
        var_0[0] += 1
        var_15[0] += 1
        var_16[0] += 1
        var_17[0] += 1
        var_14[0] += 1
        var_15[0] += 1
        var_18[0] += 1
        var_16[0] += 1
        var_19[0] += 1
        var_20[0] += 1
        var_21[0] += 1
        var_15[0] += 1
        var_22[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        found = False
        if param in end_loop_shared_vars_res:
            end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
        else:
            end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_4(var_0, var_1, var_12, var_13, var_5, var_8, var_7, var_9, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[4] += 1
        var_0[0] += 1
        var_1[0] += 1
        var_12[0] += 1
        var_13[0] += 1
        mutex_1.acquire()
        var_5[0] += 1
        mutex_1.release()
        var_8[0] += 1
        var_5[0] += 1
        mutex_2.acquire()
        var_7[0] += 1
        mutex_2.release()
        var_9[0] += 1
        var_7[0] += 1
        var_14[0] += 1
        var_0[0] += 1
        var_15[0] += 1
        var_16[0] += 1
        var_17[0] += 1
        var_14[0] += 1
        var_15[0] += 1
        var_18[0] += 1
        var_16[0] += 1
        var_19[0] += 1
        var_20[0] += 1
        var_21[0] += 1
        var_15[0] += 1
        var_22[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        found = False
        if param in end_loop_shared_vars_res:
            end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
        else:
            end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

def thread_5(var_0, var_1, var_12, var_13, var_5, var_8, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_41):
    arguments = locals()
    while not exit_loops:
        per_thread_loop_count[5] += 1
        var_0[0] += 1
        var_1[0] += 1
        var_12[0] += 1
        var_13[0] += 1
        mutex_1.acquire()
        var_5[0] += 1
        mutex_1.release()
        var_8[0] += 1
        var_5[0] += 1
        var_14[0] += 1
        var_0[0] += 1
        var_15[0] += 1
        var_16[0] += 1
        var_17[0] += 1
        var_14[0] += 1
        var_15[0] += 1
        var_18[0] += 1
        var_16[0] += 1
        var_19[0] += 1
        var_20[0] += 1
        var_21[0] += 1
        var_15[0] += 1
        var_22[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
        var_23[0] += 1
        var_20[0] += 1
        var_0[0] += 1
        var_24[0] += 1
        var_20[0] += 1
        var_41[0] += 1
    arguments_list = arguments.items()
    params = []
    for key, val in arguments_list: params.append(int(key.split("_")[1]))
    for i, param in enumerate(params):
        found = False
        if param in end_loop_shared_vars_res:
            end_loop_shared_vars_res[param].append(arguments["var_" + str(param)][0])
        else:
            end_loop_shared_vars_res[param] = [arguments["var_" + str(param)][0]]

if __name__ == "__main__":
    main()
