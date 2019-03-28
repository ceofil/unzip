#!/usr/bin/python
import threading
import time


class MyThread (threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        print('Starting ' + self.name)
        process_data(self.name)
        print('Exiting ' + self.name)


def process_data(thread_name):
    for i in range(5):
        print("{} processing info   {}   {}\n".format(thread_name, i, time.strftime('%X')))
        time.sleep(2)


threads = []
threadID = 1

# Create new threads
for i in range(3):
    thread = MyThread(threadID, "Thread {}".format(i))
    thread.start()
    threads.append(thread)
    threadID += 1


print('Exiting Main Thread')
