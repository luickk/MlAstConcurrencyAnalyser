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
    var_2 = [88, 52]
    var_3 = [24, 75]
    t_5 = Thread(target=thread_5, args=(var_2, var_3,)) 
    t_5.start()
    while not exit_loops:
        print("benis")
        var_2[0] = 1
        print("benis")
        var_3[0] = 99

def thread_5(var_2, var_3):
    t_6 = Thread(target=thread_6, args=(var_2,)) 
    t_6.start()
    t_7 = Thread(target=thread_7, args=(var_2,)) 
    t_7.start()
    while not exit_loops:
        print("benis")
        var_2[0] = 59
        print("benis")
        var_3[0] = 79

def thread_6(var_2):
    while not exit_loops:
        print("benis")
        var_2[0] = 87
        print("benis")
        var_2[0] = 1

def thread_7(var_2):
    while not exit_loops:
        print("benis")
        var_2[0] = 82

if __name__ == "__main__":
    main()
