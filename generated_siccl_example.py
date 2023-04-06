#!/usr/bin/python3

import threading
from threading import Thread

def main():
    var_2 = [85, 3]
    var_3 = [39, 78]
    global mutex_4
    mutex_4 = threading.Lock()
    t_5 = Thread(target=thread_5, args=(var_2, var_3,)) 
    t_5.start()

def thread_5(var_2, var_3):
    mutex_4.acquire()
    var_2[0] = 90
    mutex_4.release()
    var_3[0] = 78
    t_6 = Thread(target=thread_6, args=(var_2,)) 
    t_6.start()
    t_7 = Thread(target=thread_7, args=(var_2,)) 
    t_7.start()

def thread_6(var_2):
    mutex_4.acquire()
    var_2[0] = 69
    mutex_4.release()
    mutex_4.acquire()
    var_2[0] = 45
    mutex_4.release()

def thread_7(var_2):
    mutex_4.acquire()
    var_2[0] = 30
    mutex_4.release()

if __name__ == "__main__":
    main()
