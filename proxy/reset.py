
import sys,os

from osuosu import listJson, infoCache
from sharep import loadJson, writeJson, status, restartp

def printServerList(dict):
    count = 0
    strTemp = ''
    for _, value in dict.items():
        count += 1
        strTemp += '{0}---{1}\n'.format(count, value)
    print(strTemp)


def linkst(infoCacheDict):
    serveDict = loadJson(listJson, infoCacheDict['save_folder'])
    printServerList(serveDict)
    number = int(input('Select server:'))
    mark = 0
    for key, _ in serveDict.items():
        mark = mark + 1
        if mark == number:
            ssrConfig = key

    if 'ssrConfig' not in dir():
        print("Error number")
        sys.exit(0)
    
    infoCacheDict['last'] = ssrConfig
    writeJson(infoCache, infoCacheDict)

    restartp(os.path.join(infoCacheDict['save_folder'], '{}.json'.format(ssrConfig)))
    status()