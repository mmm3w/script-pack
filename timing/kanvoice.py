from json import dumps, loads
from requests import get
from os import walk, path
from html import unescape
from re import findall, search
from lxml import etree
from copy import deepcopy

from tools import checkDirectory, removeSpecialSymbol, mergeStrList, downloadFile

def obtainVoiceList(p):
    list = []
    voice = walk(p) 
    for _, _, files in voice: 
        for f in files: 
            portion = path.splitext(f)
            if portion[1] == '.json':
                list.append(portion[0])
    return list

def isVoiceNodeFromKanWiki(pppVoiceNode):
    if pppVoiceNode.xpath('normalize-space(.//th[1]/text())') == '语音':
        return True
    else:
        return False

#舰娘百科舰C语音获取
def requestVoiceFileFromKanWiki(kanUrl, savePath, kanNameKN):
    requestHeaders = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}

    print('----------------------------------\nStart')
    print('Obtain from {}'.format(kanUrl))
    res = get(kanUrl, headers = requestHeaders).content.decode('utf-8')
    etHtml = etree.HTML(res)
    kanName = etHtml.xpath('normalize-space(//h1[@id="firstHeading"])')

    print('Name:{}'.format(kanName))
    kanVoiceFolder = path.join(savePath, 'voice', kanNameKN)
    checkDirectory(kanVoiceFolder)

    voiceBlock = etHtml.xpath('.//body//div[@id="mw-content-text"]/div[@class="mw-parser-output"]/*')
    parserTag = False
    voiceSetType = ''
    voiceList = []

    defineVoiceJSFile = ''
    defineVoiceSetName = []

    #固有语音
    for blockNode in voiceBlock:
        if blockNode.xpath('normalize-space(./span/text())') == '语音资料':
            parserTag = True
            continue
        if blockNode.xpath('normalize-space(./span/text())') == '游戏资料':
            parserTag = False
            continue
        if not parserTag:
            continue
        #从这里开始
        if blockNode.tag == 'h3':
            voiceSetType = blockNode.xpath('normalize-space(./span/text())')
            if voiceSetType.count('游戏') > 0:
                parserTag = False
            else:
                print('Obtain {} voice block'.format(voiceSetType))
            continue

        voiceDect = {}

        if blockNode.tag == 'table':
            # print(len(blockNode.xpath('.//tr')))
            for voiceNode in blockNode.xpath('.//tr'):
                #跳过抬头
                if len(voiceNode.xpath('./th')) > 0:
                    continue
                if len(voiceNode.xpath('./td')) == 3:
                    voiceDect['voiceAudioUrl'] = voiceNode.xpath('normalize-space(./td[1]//a/@data-filesrc)')
                    voiceDect['voiceType'] = voiceNode.xpath('normalize-space(./td[2]//text())')
                    voiceDect['voiceTextJP'] = voiceNode.xpath('normalize-space(./td[3]//text())')
                if len(voiceNode.xpath('./td')) == 1:
                    voiceDect['voiceTextCH'] = voiceNode.xpath('normalize-space(./td//text())')
                    voiceDect['voiceSetType'] = voiceSetType
                    voiceDect['voiceAudioFile'] = downloadFile(voiceDect['voiceAudioUrl'], kanVoiceFolder + "/").split('/')[-1]
                    voiceList.append(deepcopy(voiceDect))
            continue
        if blockNode.tag == 'p' and len(blockNode.xpath('./script')) > 0:
            defineVoiceJSFile = blockNode.xpath('normalize-space(./script/@src)')

        if blockNode.tag == 'script':
            defineVoiceSetName.append(search(r'(?<=").*?(?=")', blockNode.xpath('normalize-space(.//text())')).group(0))

    #限定语音
    defineVoiceJSStr = get(defineVoiceJSFile, headers = requestHeaders).content.decode('utf-8')
    defineVoiceUrlHeader = search(r'(?<=data-filesrc=\\").*?(?=")', defineVoiceJSStr).group(0)
    defineJsonUrl = search(r'(?<=")https.*?json(?=")', defineVoiceJSStr).group(0).replace(".json","").replace("wid","").replace("\"","").replace(" ","").replace("+","")
    for defineType in defineVoiceSetName:
        try:
            defineVoiceDataStr = get("{0}{1}.json".format(defineJsonUrl, defineType), headers = requestHeaders).content.decode('utf-8')
            defineVoiceDataDect = loads(defineVoiceDataStr)
            for defineSetType in defineVoiceDataDect:
                for defineItem in defineVoiceDataDect[defineSetType]:
                    voiceDect['voiceSetType'] = defineSetType
                    voiceDect['voiceType'] = defineVoiceDataDect[defineSetType][defineItem]['vname']
                    voiceDect['voiceTextJP'] = defineVoiceDataDect[defineSetType][defineItem]['ja']
                    voiceDect['voiceTextCH'] = defineVoiceDataDect[defineSetType][defineItem]['zh']
                    voiceDect['voiceAudioUrl'] = defineVoiceUrlHeader + defineVoiceDataDect[defineSetType][defineItem]['file']
                    voiceDect['voiceAudioFile'] = downloadFile(voiceDect['voiceAudioUrl'], kanVoiceFolder + "/").split('/')[-1]
                    voiceList.append(deepcopy(voiceDect))
        except:
            continue

    jsonSaveFile = open(path.join(kanVoiceFolder, '{}.json'.format(kanNameKN)), 'w', encoding='utf-8')
    jsonSaveFile.write(dumps({'nameCH':kanName, 'nameKN':kanNameKN, 'voice':voiceList}, ensure_ascii=False))
    jsonSaveFile.close()
    print("Finish\n----------------------------------")