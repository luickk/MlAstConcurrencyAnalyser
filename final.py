#!/usr/bin/python3

from threading import Thread

def main():
    var1 = [88, 80]
    var2 = [58, 20]
    var3 = [0, 9]
    t_thread_66 = Thread(target=thread_66, args=(var1,)) 
    t_thread_66.start()
    t_thread_19 = Thread(target=thread_19, args=(var1, var2, var3,)) 
    t_thread_19.start()
    t_thread_20 = Thread(target=thread_20, args=(var3, var2,)) 
    t_thread_20.start()

def thread_66(var1):
    var1[0] = 67

def thread_19(var1, var2, var3):
    var1[0] = 35
    var2[0] = 56
    t_thread_50 = Thread(target=thread_50, args=(var2, var3, var1,)) 
    t_thread_50.start()

def thread_50(var2, var3, var1):
    var2[0] = 74
    t_thread_89 = Thread(target=thread_89, args=(var3, var1,)) 
    t_thread_89.start()

def thread_89(var3, var1):
    var3[0] = 45
    var1[0] = 7

def thread_20(var3, var2):
    var3[0] = 11
    var2[0] = 18

if __name__ == "__main__":
    main()
