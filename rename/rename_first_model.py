import os,shutil,time

hint = "y"
path = os.getcwd()
parent_path = os.path.dirname(path)
name_length = 4
jump = ".py"

print("The work directory is " + path)
topn = input("Input top:")
text = input("Please input '"+ hint +"' to do action:")

def traversalFile(rootDir):
    list_dirs = os.walk(rootDir) 
    for root, _, files in list_dirs: 
        count = int(topn)
        for f in files: 
            portion = os.path.splitext(f)
            if portion[1] not in jump:
                oldfile = os.path.join(root, f)
                newname = str(count).zfill(name_length) + portion[1]
                newfile = os.path.join(root, newname)
                os.rename(oldfile,newfile)
                print(os.path.basename(oldfile)+' -> '+ os.path.basename(newfile))
                count += 1
               

if text == hint:
    traversalFile(path)

# print("The parent directory is " + parent_path)
# targetpath =  os.path.join(parent, newname)
# shutil.move(newfile, targetpath)
# print(newfile+' move to '+ targetpath)