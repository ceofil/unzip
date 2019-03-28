#!/usr/bin/python
import threading
import time
from math import *
import random
import queue

N = 4  # number of threads
nr_of_files = 5
threads = []


class MyThread (threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.data_size = 0
        self.occupied = False
        self.time_stamp = time.time()
        self.exit_flag = False
        self.has_just_been_occupied = False

    def extract_file(self): # to simulate extracting a big file until I implement that
        time.sleep(self.data_size)
        self.occupied = False

    def occupy(self, data_size):
        print("Thread {} was occupied with {}".format(self.thread_id, data_size))
        self.occupied = True
        self.has_just_been_occupied = True
        self.time_stamp = time.time()
        self.data_size = data_size

    def run(self):
        while not self.exit_flag:
            if self.has_just_been_occupied:
                self.has_just_been_occupied = False
                self.extract_file()
        print("Thread {} has finished".format(self.thread_id))
            

files = queue.Queue()
sum_of_times = 0

start = time.time()

# add some "files" to the queue
for i in range(nr_of_files):
    size = random.randint(1, 10)
    files.put(size)
    sum_of_times += size
    print(size)

# initialize threads
for i in range(N):
    thr = MyThread(i)
    threads.append(thr)
    thr.start()


while not files.empty():
    for thread_it in threads:
        if (not files.empty()) and (not thread_it.occupied):
            thread_it.occupy(files.get())

for thread_to_kill in threads:
    thread_to_kill.exit_flag = True

for thread_to_kill in threads:
    thread_to_kill.join()

end = time.time()
print('Exiting Main Thread')
print(floor(end-start))  # if threading is working correctly this should be lower than sum_of_times
print(sum_of_times)

