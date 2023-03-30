#!/usr/bin/python3

import threading
from threading import Thread

def main():
    var1 = [51, 40]
    var2 = [52, 36]
    var3 = [90, 92]
    global m1
    m1 = threading.Lock()
    t_thread_94 = Thread(target=thread_94, args=(var1,)) 
    t_thread_94.start()
    t_thread_32 = Thread(target=thread_32, args=(var1, var2, var3,)) 
    t_thread_32.start()
    t_thread_15 = Thread(target=thread_15, args=(var3, var2,)) 
    t_thread_15.start()

def thread_94(var1):
    m1.acquire()
    var1[0] = 24
    m1.release()

def thread_32(var1, var2, var3):
    m1.acquire()
    var1[0] = 79
    m1.release()
    var2[0] = 53
    t_thread_20 = Thread(target=thread_20, args=(var2, var3, var1,)) 
    t_thread_20.start()

def thread_20(var2, var3, var1):
    var2[0] = 63
    t_thread_17 = Thread(target=thread_17, args=(var3, var1,)) 
    t_thread_17.start()

def thread_17(var3, var1):
    var3[0] = 10
    var1[0] = 9

def thread_15(var3, var2):
    var3[0] = 50
    var2[0] = 64

if __name__ == "__main__":
    main()
