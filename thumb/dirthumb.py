import sys
import os
from threading import Thread
from shutil import copyfile

def isimage(file):
    suffix = os.path.splitext(file)[-1][1:].lower()
    return suffix == "bmp" or suffix == "jpg" or suffix == "jpeg" or suffix == "png" or suffix == "gif"

def ttc(dir):
    for lists in os.listdir(dir):
        ppp = os.path.join(dir, lists)
        if os.path.isdir(ppp):
            thumb = os.path.join(ppp, '.thumb')
            if not os.path.exists(thumb):
                Thread(target=ttc, args=(ppp,)).start()
        else:
            thumb = os.path.join(dir, '.thumb')
            if not os.path.exists(thumb) and isimage(ppp):
                copyfile(ppp, thumb)

if len(sys.argv) <= 1:
    exit()
targetdir = sys.argv[1]
Thread(target=ttc, args=(targetdir,)).start()