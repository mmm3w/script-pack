
import sys
import os
import zipfile

def unzip(zipf, savedir):
    name  = os.path.basename(zipf).split('.')[0]
    td = os.path.join(savedir, name)
    if os.path.exists(td):
        if os.path.isdir(td):
            return
        else:
            os.remove(td)
    if not os.path.exists(td):
        os.mkdir(td)
    print(zipf)
    r = zipfile.is_zipfile(zipf)
    if r:
        fz = zipfile.ZipFile(zipf, 'r')
        for file in fz.namelist():
            fz.extract(file, td) 

if len(sys.argv) <= 2:
    exit()

targetdir = sys.argv[1]
zipdir = sys.argv[1]
savedir = sys.argv[2]

listdirs = os.walk(zipdir)
for root, dirs, files in listdirs:
    for f in files:
        if os.path.splitext(f)[-1][1:].lower() == "zip":
            relp = os.path.relpath(root, start=zipdir)
            td = os.path.join(savedir, relp)
            if os.path.exists(td):
                if os.path.isfile(td):
                    os.remove(td)
            if not os.path.exists(td):
                os.makedirs(td)
            unzip(os.path.join(root, f), td)
