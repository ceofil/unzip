#!/usr/bin/python
import threading
import time
from math import *
import random
import queue

N = 2  # number of threads
nr_of_files = 5
threads = []


class MyThread (threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.data_size = 0
        self.occupied = False
        self.time_stamp = time.time()

    def extract_file(self): # to simulate extracting a big file until I implement that
        time.sleep(self.data_size)

    def occupy(self, data_size):
        print("Thread {} was occupied with {}".format(self.thread_id, data_size))
        self.occupied = True
        self.time_stamp = time.time()
        self.data_size = data_size

    def run(self):
        self.extract_file()
        self.occupied = False
        print("Thread {} was freed ".format(self.thread_id))


files = queue.Queue()
suma = 0

start = time.time()

# add some "files" to the queue
for i in range(nr_of_files):
    size = random.randint(1, 3)
    files.put(size)
    suma += size
    print(size)

# initialize threads
for i in range(N):
    thr = MyThread(i)
    threads.append(thr)


while not files.empty():
    for thread_it in threads:
        if (not files.empty()) and (not thread_it.occupied):
            thread_it.occupy(files.get())
            thread_it.start()

end = time.time()
print('Exiting Main Thread')
print(floor(end-start))
print(suma)

