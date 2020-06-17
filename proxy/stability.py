import sys, os

from osuosu import localTest, internTest, logFile
from osuosu import infoCache, internRefer
from sharep import netspeed, writeLog, pidofp
from sharep import startp, obtainWeightDict, netfea
from sharep import restartp, writeWeight, writeJson

def addrpick(infoCacheDict):
    wDict = obtainWeightDict()
    for wItem in sorted(obtainWeightDict().items(),key=lambda x:x[1]):
        #判断能否够连接到代理地址
        if netfea(wItem[0].split('(')[0]):
            restartp(os.path.join(infoCacheDict['save_folder'], '{0}.json'.format(wItem[0])))
            if netspeed(internTest) > internRefer:
                wDict[wItem[0]] = wItem[1] + 1
                writeWeight(wDict)
                writeLog(logFile, 'INF: Change config({0}).'.format(wItem[0]))
                infoCacheDict['last'] = wItem[0]
                writeJson(infoCache, infoCacheDict)
                sys.exit(0)

    writeLog(logFile, 'ERR: No services available')
    sys.exit(0)

def kudzu(infoCacheDict):
    #检测网络可用性
    if not netfea(localTest):
        writeLog(logFile, 'ERR: Ping {} fail. Net maybe error'.format(localTest))
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