import os, sys, shutil
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def checkFolder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def obtainResolution(imagePath, args):
    with Image.open(imagePath) as image:
        args[0] = max(image.width, image.height)
        args[1] = min(image.width, image.height)
        if image.width == image.height:
            args[2] = 0
        else:
            args[2] = 1 if image.width > image.height else -1

def compareResolution(args, resolution, obortOrientation):
    lastResolution = "other"
    for item in resolution:
        temp = item.split('x')
        if args[0] >= int(temp[0]) and args[1] >= int(temp[1]):
            lastResolution = item
        else:
            break
    if obortOrientation:
        if args[2] == -1:
            return os.path.join(lastResolution, "vertical")
        elif args[2] == 1:
            return os.path.join(lastResolution, "horizontal")
        else:
            return os.path.join(lastResolution, "square")
    else:
        return lastResolution

#图片类型
suffix=".jpg.png"
obortOrientation = False
#分辨率分组
resolution = ["1280x720","1366x768","1600x900","1920x1080","1920x1200","2560x1440","2560x1600","3840x2160","5120x2880","7680x4320"]
path = input("Input path:")
#0:长宽中的最大值
#1:长宽中的最小值
#2:0正方形，1横向矩形，-1纵向矩形
args = [0, 0, 0]

for fileName in os.listdir(path):
    if os.path.isfile(os.path.join(path, fileName)):
        portion = os.path.splitext(fileName)
        if portion[1] in suffix:
            obtainResolution(os.path.join(path, fileName), args)
            resolutionPath = compareResolution(args, resolution, obortOrientation)
            checkFolder(os.path.join(path, resolutionPath))
            shutil.move(os.path.join(path, fileName),
                        os.path.join(path, resolutionPath, fileName))
