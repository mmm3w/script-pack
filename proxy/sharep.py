
import os, io, base64, time
import json
import subprocess

from osuosu import infoCache, statusc, startc
from osuosu import ssrpidc, stopc, curlspeedc
from osuosu import weightTemp, pingc, alnatag

################
def isCacheCreate():
    return os.path.exists(infoCache)

def obtainCache():
    with io.open(infoCache, 'r', encoding = 'utf-8') as f:
        return json.loads(f.read())

def obtainWeightDict():
    with io.open(weightTemp, 'r', encoding = 'utf-8') as f:
        mDict = {}
        for line in f:
            if '|' in line:
                w = line.replace('\n', '').split('|')
                mDict[w[1]] = int(w[0])
        return mDict

def createWeight(sList):
    with io.open(weightTemp, 'w', encoding = 'utf-8') as f:
        for sK,_ in sList.items():
            for tag in alnatag:
                if tag in sK:
                    f.write('0|{0}\n'.format(sK))


def writeWeight(wDict):
    with io.open(weightTemp, 'w', encoding = 'utf-8') as f:
        for k,v in wDict.items():
            f.write('{0}|{1}\n'.format(str(v), k))

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def writeLog(logPath, text):
    with io.open(logPath, 'a+', encoding='utf-8') as f:
        f.write('{0}\t{1}\n'.format(time.asctime(time.localtime(time.time())),text))

def writeJson(filePath, dict, workspace = ''):
    with io.open(os.path.join(workspace,filePath), 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(dict, ensure_ascii=False))

def loadJson(filePath, workspace = ''):
    with io.open(os.path.join(workspace,filePath), 'r', encoding = 'utf-8') as f:
        return json.loads(f.read())

################
def status():
    subprocess.run(statusc, shell=True)

def startp(conf):
    subprocess.run(startc.format(conf), shell=True, stdout=subprocess.DEVNULL)

def pidofp():
    return subprocess.run(ssrpidc, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')

def stoppid(pid):
    subprocess.run(stopc.format(pid), shell=True, stdout=subprocess.DEVNULL)

def stopp():
    p = pidofp()
    if len(p) > 0:
        stoppid(p)
        
def restartp(conf):
    stopp()
    startp(conf)

################
def baseEqualPadding(source):
    equalPadding = len(source) % 4
    if equalPadding != 0:
        return source + b'=' * (4 - equalPadding)
    else:
        return source

def repBase(str):
    return str.replace('_','/').replace('-','+')

def decode(str):
    return base64.b64decode(baseEqualPadding(repBase(str).encode())).decode('utf-8')

################
def netspeed(url):
    return int(subprocess.run(curlspeedc.format(url), shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8'))

def netfea(domain):
    return subprocess.run(pingc.format(domain), shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8') == '0'







