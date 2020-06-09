import os

hint = "I am sure"
path = os.getcwd() + "/"
name_length = 4
jump = ".py"

print("The work directory is " + path)
folder = input("Please input target folder:")
text = input("Please input '"+ hint +"' to do action:")

def traversalFile(rootDir):
    list_dirs = os.walk(rootDir) 
    for root, _, files in list_dirs: 
        count = 0
        for f in files: 
            portion = os.path.splitext(f)
            if portion[1] not in jump:
                count += 1
                oldname = os.path.join(root, f)
                newname = os.path.join(root, str(count).zfill(name_length)) + portion[1]
                os.rename(oldname,newname)
                print(os.path.basename(oldname)+' -> '+ os.path.basename(newname))

if text == hint:
    traversalFile(path + folder)


