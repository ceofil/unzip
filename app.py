#!/usr/bin/python
import threading
import time
from math import *
import queue
import zipfile
import os
import logging

logging.basicConfig(filename ='test.log', level=logging.INFO)
directory = 'C:\\Users\\Teofil\\Desktop\\directory'
output_dir = 'C:\\Users\\Teofil\\Desktop\\directory\\Fantasy'

files = queue.Queue()
N = 1  # number of threads
nr_of_files = 0
nr_files_extracted = 0
sum_of_file_size = 0
threads = []


class MyThread (threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.occupied = False
        self.time_stamp = time.time()
        self.exit_flag = False
        self.has_just_been_occupied = False
        self.has_just_finished = False  # update_console will be called only if this is true
        self.file_to_extract = None

    def get_elapsed_time(self):
        return floor(time.time() - self.time_stamp)

    def get_file_size(self):
        return sum(zinfo.file_size for zinfo in self.file_to_extract.filelist)

    def extract_file(self):
        self.file_to_extract.extractall(output_dir)
        self.occupied = False
        self.has_just_finished = True

    def occupy(self, file_name):
        self.file_to_extract = zipfile.ZipFile(directory + '\\' + file_name)
        self.occupied = True
        self.has_just_been_occupied = True
        self.time_stamp = time.time()

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
            print("is extracting {} of size {}".format(thr.file_to_extract.filename, thr.get_file_size()))
        elif files.empty():
            print('is FREE but the queue is empty ')
        else:
            print('is FREE ')
    print('\n\n')


def every_thread_has_finished():
    for thr in threads:
        if thr.occupied or thr.has_just_finished:
            return False
    return True


def log_thread_info(thr):
    logging.info("file {}; duration {}; size {};".format(\
        thread_it.file_to_extract.filename,\
        thread_it.get_elapsed_time(),\
        thread_it.get_file_size()))



start = time.time()

# add all the files in the queue
for s in os.listdir(directory):
    if '.zip' in s:
        files.put(s)
        nr_of_files += 1

# initialize threads
for i in range(N):
    thr = MyThread(i)
    threads.append(thr)
    thr.start()


while not files.empty():
    for thread_it in threads:
        if thread_it.has_just_finished:
            thread_it.has_just_finished = False
            nr_files_extracted += 1
            update_console()
            log_thread_info(thread_it)
            sum_of_file_size += thread_it.get_file_size()
            thread_it.file_to_extract.close()
        if (not files.empty()) and (not thread_it.occupied):
            thread_it.occupy(files.get())
            update_console()

while not every_thread_has_finished():
    for thread_it in threads:
        if thread_it.has_just_finished:
            thread_it.has_just_finished = False
            nr_files_extracted += 1
            update_console()
            log_thread_info(thread_it)
            sum_of_file_size += thread_it.get_file_size()
            if not thread_it.file_to_extract.fp:  
                thread_it.file_to_extract.close()


update_console()
for thread_to_kill in threads:
    thread_to_kill.exit_flag = True

for thread_to_kill in threads:
    thread_to_kill.join()

end = time.time()
elapsed_time = floor(end - start)
print(" Elapsed time: {}".format(elapsed_time))
logging.info("extracted {} of data in {}s with {} threads".format(sum_of_file_size, elapsed_time, N))
