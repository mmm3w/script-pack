import os

workspace = os.path.split(os.path.realpath(__file__))[0]

input_folder = workspace + "/input/"
output_folder = workspace + "/out/"
apktool = workspace + "/Tools/apktool/apktool"
jadx = workspace + "/Tools/jadx/bin/jadx"

def clearFolder(path):
    print("Clear folder : " + path)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    
def checkDirectory(dir):
    if not os.path.exists(dir):
        print("Create folder : " + dir)
        os.makedirs(dir)

def checkApkFile():
    apks = []
    for _, _, files in os.walk(input_folder):
        for f in files:
            if os.path.splitext(f)[1] == ".apk":
                apks.append(f)
    return apks

def listApk(list):
    number = 0
    for f in list:
        number += 1
        print("[{0}]{1}".format(number, f))

def decodeByApktool(file):
    print("Decode by apktool")
    portion = os.path.splitext(file)
    apktool_out_path = output_folder + portion[0] + "_apktool"
    if os.path.exists(apktool_out_path):
        clearFolder(apktool_out_path)
    else:
        os.makedirs(apktool_out_path)
    print("apktool:start ...")
    inp = (input_folder + file).replace("\\", "/")
    out = apktool_out_path.replace("\\", "/")
    os.system("{0} d {1} -f -o {2}".format(apktool, inp, out))
    print("apktool:finish")

def decodeByJadx(file):
    print("Decode by Jadx")
    portion = os.path.splitext(file)
    apktool_out_path = output_folder + portion[0] + "_jadx"
    if os.path.exists(apktool_out_path):
        clearFolder(apktool_out_path)
    else:
        os.makedirs(apktool_out_path)
    print("jadx:start ...")
    inp = (input_folder + file).replace("\\", "/")
    out = apktool_out_path.replace("\\", "/")
    os.system("{0} -d {2} -j 1 {1}".format(jadx, inp, out))
    print("jadx:finish")

input("Please enter 'Enter' to start")
print("=============================")
print("Current workspace : " + workspace)
checkDirectory(input_folder)
checkDirectory(output_folder)
print("=============================")
apks = checkApkFile()
listApk(apks)
number = input("Input apk number : ")
if number.isdigit():
    n = int(number) - 1
    if n < len(apks) and n >= 0:
        print("Start decode {}".format(apks[n]))
        print("=============================")
        decodeByApktool(apks[n])
        print("=============================")
        decodeByJadx(apks[n])
input("Finish!")


