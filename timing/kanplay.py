#语音播放
from json import loads
from os import path
from random import randrange
from playsound import playsound
from threading import Thread

from tools import playLog, timef, numberContrastTable

#欢迎语音
def welcome(kyaraName, voiceFolder):
    jsonFile = open(path.join(voiceFolder, kyaraName, '{}.json'.format(kyaraName)), 'r', encoding='utf-8')
    jsonStr = jsonFile.read()
    jsonFile.close()
    kyaraDict = loads(jsonStr)
    voiceTemp = []
    for voiceItem in kyaraDict['voice']:
        if voiceItem['voiceType'].find('登入') >= 0:
            voiceTemp.append(voiceItem)
        elif voiceItem['voiceType'].find('秘书') >= 0:
            voiceTemp.append(voiceItem)
        elif voiceItem['voiceType'].find('建造') >= 0:
            voiceTemp.append(voiceItem)
        elif voiceItem['voiceType'].find('编成') >= 0:
            voiceTemp.append(voiceItem)
        elif voiceItem['voiceType'].find('出征') >= 0:
            voiceTemp.append(voiceItem)
        elif voiceItem['voiceType'].find('图鉴') >= 0:
            voiceTemp.append(voiceItem)
        else:
            pass
    targetVoiceItem = voiceTemp[randrange(0, len(voiceTemp), 1)]
    if targetVoiceItem:
        print(path.join(voiceFolder, kyaraName, targetVoiceItem['voiceAudioFile']))
        playsound(path.join(voiceFolder, kyaraName, targetVoiceItem['voiceAudioFile']), block = False)
        return targetVoiceItem

#报时语音
def broadcast(hour, kyaraName, voiceFolder):
    jsonFile = open(path.join(voiceFolder, kyaraName, '{}.json'.format(kyaraName)), 'r', encoding='utf-8')
    jsonStr = jsonFile.read()
    jsonFile.close()
    kyaraDict = loads(jsonStr)

    timeTag = ''
    for singleNumber in list(timef(hour)):
        timeTag += numberContrastTable[singleNumber]
    timeTag += numberContrastTable['0']
    timeTag += numberContrastTable['0']

    for voiceItem in kyaraDict['voice']:
        if voiceItem['voiceType'].find(timeTag) >= 0:
            playsound(path.join(voiceFolder, kyaraName, voiceItem['voiceAudioFile']), block = True)
            return voiceItem