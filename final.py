#!/usr/bin/python3

from threading import Thread

def main():
    var1 = 50
    var2 = 67
    var3 = 13
    t_thread_77 = Thread(target=thread_77, args=()) 
    t_thread_77.start()
    t_thread_71 = Thread(target=thread_71, args=()) 
    t_thread_71.start()

def thread_77():
    var1 = 17

def thread_71():
    var1 = 14
    var2 = 20

if __name__ == "__main__":
    main()
