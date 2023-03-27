#!/usr/bin/python3

import threading
from threading import Thread

def main():
    var1 = [72, 65]
    var2 = [46, 47]
    var3 = [74, 81]
    global m1
    m1 = threading.Lock()
    t_thread_55 = Thread(target=thread_55, args=(var1,)) 
    t_thread_55.start()
    t_thread_95 = Thread(target=thread_95, args=(var1, var2, var3,)) 
    t_thread_95.start()
    t_thread_8 = Thread(target=thread_8, args=(var3, var2,)) 
    t_thread_8.start()

def thread_55(var1):
    m1.acquire()
    var1[0] = 6
    m1.release()

def thread_95(var1, var2, var3):
    m1.acquire()
    var1[0] = 1
    m1.release()
    var2[0] = 56
    t_thread_56 = Thread(target=thread_56, args=(var2, var3, var1,)) 
    t_thread_56.start()

def thread_56(var2, var3, var1):
    var2[0] = 82
    t_thread_42 = Thread(target=thread_42, args=(var3, var1,)) 
    t_thread_42.start()

def thread_42(var3, var1):
    var3[0] = 12
    var1[0] = 2

def thread_8(var3, var2):
    var3[0] = 87
    var2[0] = 74

if __name__ == "__main__":
    main()
