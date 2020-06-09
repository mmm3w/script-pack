#后台脚本，建议加入开机计划任务
#need playsound module
import sys
from time import time, localtime
from threading import Timer
from os import path
from kanplay import broadcast, welcome
from tools import timef, playLog

intervalTime = 60 #mins
workspace = path.split(path.realpath(__file__))[0]
voiceFolder = path.join(workspace, "voice")
logFilePath = path.join(workspace, 'timing.log')
kyara = ''

def byTheTime(bHour):
    global voiceFolder
    global logFilePath
    global kyara
    refreshKr()
    roofread()
    try:
        targetBroadcastVoice = broadcast(bHour, kyara, voiceFolder)
        if targetBroadcastVoice:
           playLog(logFilePath, 'Broadcast', '{0}:{1} {2}'.format(kyara, targetBroadcastVoice['voiceTextJP'],  targetBroadcastVoice['voiceAudioFile']))
    except Exception as e:
        playLog(logFilePath, 'Error', e)
        pass

def roofread():
    global intervalTime
    global logFilePath
    lt = localtime(time())
    Timer(interval = (intervalTime - lt.tm_min) * 60 - lt.tm_sec, function = byTheTime, args = (lt.tm_hour, )).start()
    playLog(logFilePath, 'Ready', 'Next time:{0}:00'.format(timef(lt.tm_hour)))

def refreshKr():
    global kyara
    global workspace
    global logFilePath
    global voiceFolder
    try:
        confFile = open(path.join(workspace, 'voice.conf'), 'r', encoding='utf-8')
        kyara = confFile.read()
        confFile.close()
    except Exception as e:
        playLog(logFilePath, 'Error', e)
        sys.exit()
    
if path.exists(path.join(workspace, 'voice.conf')):
    refreshKr()
    roofread()
    try:
       targetWelcomeVoice = welcome(kyara, voiceFolder)
       if targetWelcomeVoice:
           playLog(logFilePath, 'Welcome', '{0}:{1} {2}'.format(kyara, targetWelcomeVoice['voiceTextJP'],  targetWelcomeVoice['voiceAudioFile']))
    except Exception as e:
        playLog(logFilePath, 'Error', e)
        pass
else:
    sys.exit()
    pass