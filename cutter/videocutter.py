import sys
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip
from threading import Thread

def cutsave(fff, start, end, videoclip):
    video = CompositeVideoClip([videoclip.subclip(start, end)])
    video.write_videofile(fff, threads = 8)

if len(sys.argv) <= 2:
    exit()
videofile = sys.argv[1]
portion = os.path.splitext(os.path.basename(videofile))
last = 0
count = 0
videoclip = VideoFileClip(videofile)
for item in sys.argv[2:]:
    save = os.path.join(os.path.dirname(videofile),
                        "-{0}".format(count).join(portion))
    end = int(item)
    cutsave(save, last, end - 1, videoclip)
    last = end
    count += 1

save = os.path.join(os.path.dirname(videofile),
                    "-{0}".format(count).join(portion))
cutsave(save, last, None, videoclip)
