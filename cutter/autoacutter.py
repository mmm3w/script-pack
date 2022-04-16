import json
import sys
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

def cutsave(fff, start, end, videoclip):
    video = CompositeVideoClip([videoclip.subclip(start, end)])
    video.write_videofile(fff)

def handleconfig(dir, config):
    for item in config:
        videofile = os.path.join(dir, item['file'])
        if os.path.exists(videofile) and os.path.isfile(videofile):
            print("Handle file:{0}".format(videofile))
            portion = os.path.splitext(item['file'])
            videoclip = VideoFileClip(videofile)
            count = 0
            for part in item['part']:
                save = os.path.join(
                    dir, "-{0}".format(count).join(portion))
                start = part['start']
                end = part['end']
                if end == -1:
                    end = None
                cutsave(save, start, end, videoclip)
                count += 1

if len(sys.argv) <= 1:
    exit()
targetdir = sys.argv[1]
for p, _, filelist in os.walk(targetdir):
    for filename in filelist:
        if filename == 'cut.json':
            with open(os.path.join(p, filename), 'rb') as f:
                cutconfig = json.loads(f.read())
            handleconfig(p, cutconfig)
