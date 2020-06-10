import os, io, sys
from json import loads

def readJson2Dict(path):
    jsonFileStr = ''
    with io.open(path, 'r', encoding='utf-8') as f:
        jsonFileStr = f.read()
    return loads(jsonFileStr)


workspace = os.path.split(os.path.realpath(__file__))[0]
subTemp = os.path.join(workspace,'sub.temp')

confFolder = ''
with io.open(subTemp, 'r', encoding='utf-8') as f:
    confFolder = f.readline().replace('\n','')

serveDict = {}
with io.open(os.path.join(confFolder, 'list.json'), 'r', encoding='utf-8') as f:
    serveDict = loads(f.read())
    
mark = 0
for key, value in serveDict.items():
    mark = mark + 1
    print('[{0}]\t{1}'.format(mark, value))

number = int(input('Select server:'))

mark = 0
for key, value in serveDict.items():
    mark = mark + 1
    if mark == number:
        ssrConfigPath = os.path.join(confFolder, '{}.json'.format(key))

if 'ssrConfigPath' not in dir():
    print("Error number")
    sys.exit(0)

if os.system('sudo kill -9 $(pidof ssr-redir)') == 0:
    print('Closed proxy process')

if os.system('(ssr-redir -c {0} -u </dev/null &>>/var/log/ssr-redir.log &)'.format(ssrConfigPath)) == 0:
    print('Restart proxy process')

os.system('sudo ss-tproxy status')