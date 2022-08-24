import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from support.download import downloadfile
from lxml import etree
import requests

retrymark = True

def analyzetitle(html):
    titleNode =  html.xpath('//h1[@class="post__title"]')
    lst = []
    for e in titleNode:
        lst.append(str(e.xpath('string(.)')).replace('\n','').strip())
    return ''.join(lst)
    
def analyzedata(html):
    data = []
    
    imageFileNodes = html.xpath('//div[@class="post__thumbnail"]/a/@href')
    nameLen = len(str(len(imageFileNodes)))
    index = 1
    for imageNode in imageFileNodes:
        data.append({"name":str(index).zfill(nameLen) + imageNode[-4:], "url":"https://kemono.party" + imageNode})
        index+=1
    
    downloadNodes = html.xpath('//a[@class="post__attachment-link"]')
    for file in downloadNodes:
        text = ''.join(file.xpath('text()')).replace('\n','').strip()[9:]
        href = ''.join(file.xpath('@href')).replace('\n','').strip()
        data.append({"name":text, "url":"https://kemono.party" + href})

    return data

def downloaddata(session, dir, list):
    global retrymark
    success = []
    failure = []
    for item in list:
        result = downloadfile(session, item['url'], dir, item['name'])
        if len(result) == 0:
            failure.append(item)
        else:
            success.append(item)
        print('[success/failure/total]:{0}/{1}/{2}'.format(
            len(success), len(failure), len(list)))
    if len(failure) != 0:
        if retrymark:
            retrymark = False
            print("Retry download failed source.")
            downloaddata(session,dir, failure)

if len(sys.argv) > 1:
    savedir = sys.argv[1]
    if len(savedir) == 0:
        savedir = os.path.split(os.path.realpath(__file__))[0]
else:
    savedir = os.path.split(os.path.realpath(__file__))[0]
s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
while 1:
    try:
        retrymark = True
        ruk = ''.join(input("Input kemono url:").split())
        if len(ruk) == 0:
            break
        # headers['referer'] = ruk
        s.headers = headers
        result = s.get(ruk)
        if result.status_code == 200:
            html = etree.HTML(result.text)
            #创建对应文件夹
            title = analyzetitle(html)
            sd = os.path.join(savedir, title)
            if os.path.exists(sd):
                if os.path.isfile(sd):
                    os.remove(sd)
                    os.makedirs(sd)
            else:
                os.makedirs(sd)
            data = analyzedata(html)
            downloaddata(s, sd, data)
        else:
            print('request error:' + result.status_code + '--->' + result.reason)
    except Exception as e:
        print(e)
input()