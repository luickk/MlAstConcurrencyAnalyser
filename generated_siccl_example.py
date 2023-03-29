#!/usr/bin/python3

import threading
from threading import Thread

def main():
    var1 = [87, 50]
    var2 = [71, 66]
    var3 = [14, 60]
    global m1
    m1 = threading.Lock()
    t_thread_14 = Thread(target=thread_14, args=(var1,)) 
    t_thread_14.start()
    t_thread_57 = Thread(target=thread_57, args=(var1, var2, var3,)) 
    t_thread_57.start()
    t_thread_98 = Thread(target=thread_98, args=(var3, var2,)) 
    t_thread_98.start()

def thread_14(var1):
    m1.acquire()
    var1[0] = 82
    m1.release()

def thread_57(var1, var2, var3):
    m1.acquire()
    var1[0] = 55
    m1.release()
    var2[0] = 93
    t_thread_87 = Thread(target=thread_87, args=(var2, var3, var1,)) 
    t_thread_87.start()

def thread_87(var2, var3, var1):
    var2[0] = 70
    t_thread_57 = Thread(target=thread_57, args=(var3, var1,)) 
    t_thread_57.start()

def thread_57(var3, var1):
    var3[0] = 17
    var1[0] = 66

def thread_98(var3, var2):
    var3[0] = 100
    var2[0] = 61

if __name__ == "__main__":
    main()
