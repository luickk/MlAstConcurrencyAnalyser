#!/usr/bin/python3

import threading
from threading import Thread

def main():
    var1 = [23, 7]
    var2 = [100, 77]
    global m1
    m1 = threading.Lock()
    t_thread1 = Thread(target=thread1, args=(var1, var2,)) 
    t_thread1.start()

def thread1(var1, var2):
    m1.acquire()
    var1[0] = 67
    m1.release()
    var2[0] = 22
    t_thread2 = Thread(target=thread2, args=(var1,)) 
    t_thread2.start()
    t_thread3 = Thread(target=thread3, args=(var1,)) 
    t_thread3.start()

def thread2(var1):
    m1.acquire()
    var1[0] = 0
    m1.release()
    m1.acquire()
    var1[0] = 82
    m1.release()

def thread3(var1):
    m1.acquire()
    var1[0] = 75
    m1.release()

if __name__ == "__main__":
    main()
