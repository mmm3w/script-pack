import os, io, sys
from tools import reStartProxy,obtainConfFolder
from json import loads,dumps

workspace = os.path.split(os.path.realpath(__file__))[0]
subTemp = os.path.join(workspace,'sub.temp')

confFolder = obtainConfFolder(subTemp)

serveDict = {}
with io.open(os.path.join(confFolder, 'list.json'), 'r', encoding='utf-8') as f:
    serveDict = loads(f.read())
    
mark = 0
for key, value in serveDict.items():
    mark = mark + 1
    print('[{0}]\t{1}'.format(mark, value))

number = int(input('Select server:'))

mark = 0
for key, value in serveDict.items():
    mark = mark + 1
    if mark == number:
        ssrConfig = key

if 'ssrConfig' not in dir():
    print("Error number")
    sys.exit(0)

serverDict = {}
with io.open(os.path.join(workspace,'server.temp'), 'r', encoding='utf-8') as f:
    serverDict = loads(f.read())
    serverDict['last'] = ssrConfig
with io.open(os.path.join(workspace,'server.temp'), 'w', encoding='utf-8') as f:
    f.write(dumps(serverDict, ensure_ascii=False))

reStartProxy(os.path.join(confFolder, '{}.json'.format(ssrConfig)))
os.system('sudo ss-tproxy status')