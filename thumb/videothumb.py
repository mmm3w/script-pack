import sys
import os
import cv2
from threading import Thread


def isvideo(fff):
    suffix = os.path.splitext(fff)[-1][1:].lower()
    return suffix == "mp4" or suffix == "avi" or suffix == "wmv" or suffix == "mkv" or suffix == "webm"


def createthumb(fff, td):
    thumbname = os.path.basename(fff) + ".jpg"
    thumbfile = os.path.join(td, thumbname)
    if os.path.exists(thumbfile):
        return

    cap = cv2.VideoCapture(fff)
    rate = cap.get(5)  # 帧速率
    framenumber = cap.get(7)  # 视频文件的帧数
    duration = framenumber / rate
    if duration > 10:
        cap.set(cv2.CAP_PROP_POS_FRAMES, rate * 10 - 1)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = cap.read()
    if ret:
        cv2.imencode('.jpg', frame)[1].tofile(thumbfile)
    cap.release()


def ttc(dir):
    for lists in os.listdir(dir):
        ppp = os.path.join(dir, lists)
        if os.path.isdir(ppp):
            Thread(target=ttc, args=(ppp,)).start()
        else:
            if isvideo(ppp):
                thumbdir = os.path.join(dir, ".videothumb")
                if os.path.exists(thumbdir) and os.path.isfile(thumbdir):
                    os.remove(thumbdir)
                if not os.path.exists(thumbdir):
                    os.mkdir(thumbdir)
                Thread(target=createthumb, args=(ppp, thumbdir,)).start()


if len(sys.argv) <= 1:
    exit()
targetdir = sys.argv[1]
Thread(target=ttc, args=(targetdir,)).start()
