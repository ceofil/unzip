import queue
import os
import time

L = queue.Queue()


for s in os.listdir('C:\\Users\\Teofil\\Desktop\\directory'):
    if '.zip' in s:
        L.put(s)


while not L.empty():
    print(L.get())


start_time = time.time()
time.sleep(62);
elapsed_time = time.time() - start_time

print(elapsed_time)
