import queue
import os


L = queue.Queue()


for s in os.listdir('C:\\Users\\Teofil\\Desktop\\directory'):
    if '.zip' in s:
        L.put(s)


while not L.empty():
    print(L.get())