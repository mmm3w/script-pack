#人気のVOCALOID From niconico
import os, requests, sys
from lxml import etree
from time import time, localtime, asctime

workspace = os.path.split(os.path.realpath(__file__))[0]
requestHeaders = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
proxies = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", } 
#VOCALOID神話入り
shinwaUrl = 'https://www.nicovideo.jp/tag/VOCALOID%E7%A5%9E%E8%A9%B1%E5%85%A5%E3%82%8A?page={}&sort=h&order=d'
#VOCALOID伝説入り
densetsuUrl = 'https://www.nicovideo.jp/tag/VOCALOID%E4%BC%9D%E8%AA%AC%E5%85%A5%E3%82%8A?page={}&sort=h&order=d'
#VOCALOID殿堂入り（数量较多，不建议获取）
dendoUrl = 'https://www.nicovideo.jp/tag/VOCALOID%E6%AE%BF%E5%A0%82%E5%85%A5%E3%82%8A?page={}&sort=h&order=d'

def obtainNicoNicoData(MDFileName, ws, url):
    markFilePath = os.path.join(ws, 'mark.temp')
    if os.path.exists(markFilePath):
        markFile = open(markFilePath, 'r', encoding='utf-8')
        markStr = markFile.read()
        markFile.close()
        try:
            mark = int(markStr)
        except:
            mark = 1
    else:
        mark = 1
    if os.path.exists(os.path.join(workspace, MDFileName)):
        mode = 'r+'
    else:
        mode = 'w'
    mdFile = open(os.path.join(workspace, MDFileName), mode, encoding='utf-8')
    if mark == 1:
        mdFile.write('sm号|标题|投稿日\n')
        mdFile.write('---|---|---\n')
    else:
        mdFile.seek(0, 2)

    global requestHeaders
    global proxies
    while mark != -1:
        try:#单次请求抓异常
            print('Request url:{}'.format(url.format(mark)))
            res = requests.get(url.format(mark), headers = requestHeaders, proxies = proxies)
            etHtml = etree.HTML(res.content.decode('utf-8'))
            videoNodes = etHtml.xpath('.//li[@class="item" and contains(@data-video-id, "sm") and contains(@data-video-item, "") and contains(@data-nicoad-video, "")]')
            if len(videoNodes) == 0:#节点没有之后说明是最后一页了，关闭文件并跳出循环
                mdFile.write('\n\nlast update:{}'.format(asctime(localtime(time()))))
                mdFile.close()
                if os.path.exists(markFilePath):
                    os.remove(markFilePath) #移除的缓存tag
                mark = -1
            else:#节点内容还有，则进行解析
                totalStr = ''
                for node in videoNodes:
                    timeStr = node.xpath('normalize-space(.//span[@class="time"]/text())')
                    smStr = node.xpath('normalize-space(./@data-video-id)')
                    titleStr = node.xpath('normalize-space(.//p[@class="itemTitle"]/a/text())').replace('|', '\|')
                    totalStr += '{0}|{1}|{2}\n'.format(smStr, titleStr, timeStr)
                #解析完成之后再写入文件
                mdFile.write(totalStr)
                mark += 1
        except Exception as e:
            #捕获请求或其他异常，缓存当前tag，保证下次重启能够继续请求
            print(e) 
            markFile = open(markFilePath, 'w', encoding='utf-8')
            markFile.write(str(mark))
            markFile.close()

            mdFile.close()
            sys.exit()

# obtainNicoNicoData('densetsu.md', workspace, densetsuUrl)
    
obtainNicoNicoData('shinwa.md', workspace, shinwaUrl)