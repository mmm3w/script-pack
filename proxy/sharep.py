
import os, io, base64
import json
import subprocess

from osuosu import infoCache, statusc, startc
from osuosu import ssrpids, stopc

########com########
def isCacheCreate():
    return os.path.exists(infoCache)

def obtainCache():
    with io.open(infoCache, 'r', encoding = 'utf-8') as f:
        return json.loads(f.read())

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

################
def status():
    subprocess.run(statusc, shell=True)

def startp(conf):
    subprocess.run(startc.format(conf), shell=True, stdout=subprocess.DEVNULL)

def pidofp():
    return subprocess.run(ssrpids, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')

def stoppid(pid):
    subprocess.run(stopc.format(pid), shell=True, stdout=subprocess.DEVNULL)

def stopp():
    p = pidofp()
    if len(p) > 0:
        stoppid(p)
        
def restartp(conf):
    stopp()
    startp(conf)

########json########
def writeJson(filePath, dict, workspace = ''):
    with io.open(os.path.join(workspace,filePath), 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(dict, ensure_ascii=False))

def loadJson(filePath, workspace = ''):
    with io.open(os.path.join(workspace,filePath), 'r', encoding = 'utf-8') as f:
        return json.loads(f.read())
################

########base64########
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








