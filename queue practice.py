import queue
import os
import time
import zipfile
start_time = time.time()

directory = 'C:\\Users\\Teofil\\Desktop\\directory'
output_dir = 'C:\\Users\\Teofil\\Desktop\\directory\\Fantasy'

L = queue.Queue()
for s in os.listdir(directory):
    if '.zip' in s:
        L.put(s)


while not L.empty():
    path = directory + '\\' + L.get()
    fantasy_zip = zipfile.ZipFile(path)
    fantasy_zip.extractall(output_dir)
    fantasy_zip.getinfo()
    print(path)
    fantasy_zip.close()

elapsed_time = time.time() - start_time
print(elapsed_time)
