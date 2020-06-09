import os
from rename_pack import Conf,rename

hint = "y"
path = 'F:/GithubFile/linux-script-pack/rename/conf.txt'
workspace = os.path.split(os.path.realpath(__file__))[0]

print("The workspace is {0}".format(workspace))

renameConf = Conf(path)

nowFolder = ''
if renameConf.isAssignFolder() == False:
    nowFolder = input("Input target folder:")
else:
    if renameConf.assignFolder == 'workspace':
        nowFolder = workspace
    else:
        nowFolder = renameConf.assignFolder
    print("Target folder:{0}".format(nowFolder))

topNumber = 0
if renameConf.renameMode == 2:
    topNumber = int(input('Input top:'))

prefix = ''
if renameConf.renameMode == 3:  
    prefix = input('Input header:')

text = input("Input '"+ hint +"' to do action:")

if text == hint:
    rename(renameConf, nowFolder, topNumber, prefix)
else:
    print('Cancel')
