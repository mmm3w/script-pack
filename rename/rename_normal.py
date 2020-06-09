import os,shutil,time

hint = "y"
path = os.getcwd()
name_length = 4
jump = ".py"

print("The work directory is " + path)
text = input("Please input '"+ hint +"' to do action:")

def traversalFile(rootDir):
    list_dirs = os.walk(rootDir) 
    for root, _, files in list_dirs: 
        count = 0
        for f in files: 
            portion = os.path.splitext(f)
            if portion[1] not in jump:
                count += 1
                oldfile = os.path.join(root, f)
                newname = str(count).zfill(name_length) + portion[1]
                newfile = os.path.join(root, newname)
                os.rename(oldfile,newfile)
                print(os.path.basename(oldfile)+' -> '+ os.path.basename(newfile))

if text == hint:
    traversalFile(path)