'''
import zipfile
zip_ref = zipfile.ZipFile('6.zip', 'r')
zip_ref.extractall();
zip_ref.close()
'''

import zipfile
fantasy_zip = zipfile.ZipFile('C:\\Users\\Teofil\\PycharmProjects\\unzip\\6.zip')
fantasy_zip.extractall('C:\\Users\\Teofil\\PycharmProjects\\unzip\\Fantasy')

fantasy_zip.close()

'''
#!/usr/bin/python

import threading
import time

def worker():
    """thread worker function"""
    time.sleep(10);
    print ('Worker')
    return

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
'''