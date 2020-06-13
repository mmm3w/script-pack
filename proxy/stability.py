import sys, os

from osuosu import localTest, internTest, logFile
from osuosu import infoCache, internRefer
from sharep import netspeed, writeLog, pidofp
from sharep import startp, obtainWeightDict, netfea
from sharep import restartp, writeWeight, writeJson

def addrpick(infoCacheDict):
    wDict = sorted(obtainWeightDict().items(),key=lambda x:x[1])
    for wK,_ in wDict:
        #判断能否够连接到代理地址
        if netfea(wK):
            restartp(os.path.join(infoCacheDict['save_folder'], '{0}.json'.format(wK)))
            if netspeed(internTest) > internRefer:
                wDict[wK] += 1
                writeWeight(wDict)
                writeLog(logFile, 'INF: Change config({0}).'.format(wK))
                infoCacheDict['last'] = wK
                writeJson(infoCache, infoCacheDict)
                sys.exit(0)

    writeLog(logFile, 'ERR: No services available')
    sys.exit(0)

def kudzu(infoCacheDict):
    #检测网络可用性
    if netspeed(localTest) <= 0:
        writeLog(logFile, 'ERR: Request {} fail. Net maybe error'.format(localTest))
        sys.exit(0)

    if int(pidofp()) < 0:
        #此时代理未开启
        if len(infoCacheDict['last']) > 0:
            startp(os.path.join(infoCacheDict['save_folder'], '{}.json'.format(infoCacheDict['last'])))
        else:
            #缺少前次启动用配置
            writeLog(logFile, 'ERR: No config cache')
            sys.exit(0)

    #检测代理速度
    if netspeed(internTest) > internRefer:
        writeLog(logFile, 'INF: Proxy normally.')
        sys.exit(0)
    else:
        addrpick(infoCacheDict)