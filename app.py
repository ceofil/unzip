#!/usr/bin/python
import threading
import time
from math import *
import random
import queue
import zipfile
import os

files = queue.Queue()
sum_of_times = 0
N = 4  # number of threads
nr_of_files = 12
nr_files_extracted = 0
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
        self.has_just_finished = False # update_console will be called only if this is true
        self.file = None

    def extract_file(self): # to simulate extracting a big file until I implement that
        time.sleep(self.data_size)
        self.occupied = False
        self.has_just_finished = True

    def occupy(self, data_size):
        self.occupied = True
        self.has_just_been_occupied = True
        self.time_stamp = time.time()
        self.data_size = data_size

    def run(self):
        while not self.exit_flag:
            if self.has_just_been_occupied:
                self.has_just_been_occupied = False
                self.extract_file()


def update_console():
    os.system('cls')
    print(" {} / {} files extracted".format(nr_files_extracted, nr_of_files))
    for thr in threads:
        print("Thread {}".format(thr.thread_id), end=' ')
        if thr.occupied:
            print("is extracting a file of size {}".format(thr.data_size))
        elif files.empty():
            print('is FREE but the queue is empty ')
        else:
            print('is FREE ')


def every_thread_has_finished():
    for thr in threads:
        if thr.occupied:
            return False
    return True


start = time.time()

# add some "files" to the queue
for i in range(nr_of_files):
    size = random.randint(1, 5)
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
            update_console()
        elif thread_it.has_just_finished:
            thread_it.has_just_finished = False
            nr_files_extracted += 1
            update_console()

while not every_thread_has_finished():
    for thread_it in threads:
        if thread_it.has_just_finished:
            thread_it.has_just_finished = False
            nr_files_extracted += 1
            update_console()


update_console()
for thread_to_kill in threads:
    thread_to_kill.exit_flag = True

for thread_to_kill in threads:
    thread_to_kill.join()

end = time.time()
print(floor(end-start))  # if threading is working correctly this should be lower than sum_of_times
print(sum_of_times)

