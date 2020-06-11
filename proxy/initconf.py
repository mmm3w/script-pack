import os, io, sys
from json import loads
from shutil import copyfile

workspace = os.path.split(os.path.realpath(__file__))[0]
subTemp = os.path.join(workspace,'sub.temp')
serverTemp = os.path.join(workspace,'server.temp')
initConf = os.path.join(workspace, 'init.json')

confFolder = ''

if os.path.exists(subTemp):
    with io.open(subTemp, 'r', encoding='utf-8') as f:
        confFolder = f.readline().replace('\n', '')
else:
    print('You should get config from subscription first.')
    sys.exit(0)

initConfDect = {}
with io.open(initConf, 'r', encoding='utf-8') as f:
    initConfDect = loads(f.read())

if not os.path.exists(initConfDect['conf'] + '.backup'):
    copyfile(initConfDect['conf'], initConfDect['conf'] + '.backup')

newConf = ''
serverList = ''
portList = ''
with io.open(serverTemp, 'r', encoding='utf-8') as lt:
    mDict = loads(lt.read())
    serverList = mDict['server']
    portList =  mDict['port']

with io.open(initConfDect['conf'] + '.backup', 'r', encoding='utf-8') as f:
    for line in f:
        #mode参数
        if 'mode' in line:
            if initConfDect['mode'] in line and '#' == line[0]:
                line = line[1:]
            if  initConfDect['mode'] not in line and '#' != line[0]:
                line = '#' + line
        
        if 'ipv4=' in line:
            line = line[:line.find("'") + 1] + initConfDect['ipv4'] + line[line.rfind("'"):]
        if 'ipv6=' in line:
            line = line[:line.find("'") + 1] + initConfDect['ipv6'] + line[line.rfind("'"):]
        if 'tproxy=' in line:
            line = line[:line.find("'") + 1] + initConfDect['tproxy'] + line[line.rfind("'"):]
        if 'tcponly=' in line:
            line = line[:line.find("'") + 1] + initConfDect['tcponly'] + line[line.rfind("'"):]
        if 'selfonly=' in line:
            line = line[:line.find("'") + 1] + initConfDect['selfonly'] + line[line.rfind("'"):]
        
        if 'proxy_svraddr4=' in line:
            line = line[:line.find("(") + 1] + serverList + line[line.rfind(")"):]
        if 'proxy_svrport=' in line:
            line = line[:line.find("'") + 1] + portList + line[line.rfind("'"):]
        
        if 'proxy_startcmd=' in line:
            line = line[:line.find("'") + 1] + 'true' + line[line.rfind("'"):]
        if 'proxy_stopcmd=' in line:
            line = line[:line.find("'") + 1] + 'true' + line[line.rfind("'"):]
        
        if 'dnsmasq_bind_port=' in line:
            line = line[:line.find("'") + 1] + str(initConfDect['dnsmasq_bind_port']) + line[line.rfind("'"):]
                        
        newConf += line


with io.open(initConfDect['conf'], 'w', encoding='utf-8') as f:
    f.write(newConf)