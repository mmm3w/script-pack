import sys
import os
import shutil
from threading import Thread

def ttc(dir):
    t = os.path.join(dir, '.thumbcache')
    if os.path.exists(t):
        shutil.rmtree(t)

    for lists in os.listdir(dir):
        ppp = os.path.join(dir, lists)
        if os.path.isdir(ppp):
            Thread(target=ttc, args=(ppp,)).start()


if len(sys.argv) <= 1:
    exit()
targetdir = sys.argv[1]
Thread(target=ttc, args=(targetdir,)).start()
