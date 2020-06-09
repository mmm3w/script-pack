import os

#遍历文件夹
#path 文件夹路径
#tsub 是否遍历子目录
#重命名回调，会获得一个file path的参数
def traversalFolder(path, tsub, ignore, rename):
    if tsub == False:
        fileCounter = 0
        for fileName in os.listdir(path):
            if os.path.isfile(os.path.join(path, fileName)):
                portion = os.path.splitext(fileName)
                if portion[1] not in ignore:
                    rename(path, fileCounter, portion[0], portion[1])
                    fileCounter += 1
    else:
        for root,_,files in os.walk(path):
            fileCounter = 0
            for fileName in files:
                portion = os.path.splitext(fileName)
                if portion[1] not in ignore:
                    rename(root, fileCounter, portion[0], portion[1])
                    fileCounter += 1


def rename(conf, folderPath, topNumber, prefix):

    def normal(folder, num, name, suffix):
        oldfile = os.path.join(folder, name + suffix)
        newname = str(num + 1).zfill(conf.nameLength) + suffix
        newfile = os.path.join(folder, newname)
        os.rename(oldfile,newfile)
        print(os.path.basename(oldfile)+' -> '+ os.path.basename(newfile))
    

    def conti(folder, num, name, suffix):
        temp = num + topNumber
        oldfile = os.path.join(folder, name + suffix)
        newname = str(temp).zfill(conf.nameLength) + suffix
        newfile = os.path.join(folder, newname)
        os.rename(oldfile,newfile)
        print(os.path.basename(oldfile)+' -> '+ os.path.basename(newfile))


    def insert(folder, num, name, suffix):
        oldfile = os.path.join(folder, name + suffix)
        newname = prefix + '-' + str(num + 1).zfill(conf.nameLength) + suffix
        newfile = os.path.join(folder, newname)
        os.rename(oldfile,newfile)
        print(os.path.basename(oldfile)+' -> '+ os.path.basename(newfile))


    if conf.renameMode == 1:
        traversalFolder(folderPath, conf.isTraverseSub, conf.ignore, normal)
    elif conf.renameMode == 2:
        traversalFolder(folderPath, conf.isTraverseSub, conf.ignore, conti)
    elif conf.renameMode == 3:
        traversalFolder(folderPath, conf.isTraverseSub, conf.ignore, insert)
    else:
        print('Mode Error')


class Conf:
    def __init__(self, confFile):
        with open(confFile, mode='r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                if '#' in line:
                    line = f.readline()
                    continue

                conf = line.replace('\n', '').split('=')

                if conf[0] == 'AssignFolder':
                    self.assignFolder = str(conf[1])
                elif conf[0] == 'Ignore':
                    self.ignore = str(conf[1])
                elif conf[0] == 'Mode':
                    self.renameMode = int(conf[1])
                elif conf[0] == 'NameLength':
                    self.nameLength = int(conf[1])
                elif conf[0] == 'TraverseSub':
                    self.isTraverseSub = bool(conf[1])

                line = f.readline()

    def isAssignFolder(self):
        return not len(self.assignFolder) == 0