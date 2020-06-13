import sys, os

from sharep import isCacheCreate, obtainCache, writeJson
from sharep import resstt, writeLog
from osuosu import infoCache, logFile
from obtain import burst
from reset import linkst
from initconf import syoukan
from stability import kudzu

def printHelp():
    print('ob:\t获取代理订阅内容')
    print('init:\t初始化ss-tproxy配置文件')
    print('set:\t设置代理服务器')
    print('ck:\t检测代理状态以及自动切换服务器')
    print('autoob:\t用于自动更新订阅，在计划任务中应用此项')

def init():
    if isCacheCreate():
        return obtainCache()
    else:
        infoCacheDict = {}
        infoCacheDict['sub_url'] = ''
        infoCacheDict['save_folder'] = ''
        infoCacheDict['server'] = ''
        infoCacheDict['port'] = ''
        infoCacheDict['last'] = ''
        writeJson(infoCache, infoCacheDict)
        return infoCacheDict

if __name__ == "__main__":
    if len(sys.argv) != 2:
        printHelp()
        sys.exit(0)

    infoCacheDict = init()
    if sys.argv[1] == 'ob':
        burst(infoCacheDict)
    elif sys.argv[1] == 'init':
        syoukan(infoCacheDict)
    elif sys.argv[1] == 'set':
        linkst(infoCacheDict)
    elif sys.argv[1] == 'ck':
        kudzu(infoCacheDict)
    elif sys.argv[1] == 'autoob':
        burst(infoCacheDict)
        syoukan(infoCacheDict)
        resstt()
        writeLog(logFile, 'INF: Update sub')
    else:
        printHelp()