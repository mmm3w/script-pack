import sys
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip
from threading import Thread

def cutsave(fff, start, end, ssss):
    videoclip = VideoFileClip(ssss)
    video = CompositeVideoClip([videoclip.subclip(start, end)])
    video.write_videofile(fff)


if len(sys.argv) <= 2:
    exit()
videofile = sys.argv[1]
portion = os.path.splitext(os.path.basename(videofile))
last = 0
count = 0
for item in sys.argv[2:]:
    save = os.path.join(os.path.dirname(videofile),
                        "-{0}".format(count).join(portion))
    end = int(item)
    Thread(target=cutsave, args=(save, last, end - 1, videofile)).start()
    last = end
    count += 1

save = os.path.join(os.path.dirname(videofile),
                    "-{0}".format(count).join(portion))
Thread(target=cutsave, args=(save, last, None, videofile)).start()
