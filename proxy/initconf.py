import os, io, sys
from shutil import copyfile

from osuosu import initConf
from sharep import loadJson

def syoukan(infoCacheDict):
    if len(infoCacheDict['server']) <= 0:
        print('You should get config from subscription first.')
        sys.exit(0)
    if not os.path.exists(initConf):
        print('You need create file:{}.'.format(initConf))
        sys.exit(0)
    initConfDect = loadJson(initConf)

    #备份配置文件
    if not os.path.exists(initConfDect['conf'] + '.backup'):
        copyfile(initConfDect['conf'], initConfDect['conf'] + '.backup')
    #获取内容并修改
    newConf = ''
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
                line = line[:line.find("(") + 1] + infoCacheDict['server'] + line[line.rfind(")"):]
            if 'proxy_svrport=' in line:
                line = line[:line.find("'") + 1] + infoCacheDict['port'] + line[line.rfind("'"):]
        
            if 'proxy_startcmd=' in line:
                line = line[:line.find("'") + 1] + 'true' + line[line.rfind("'"):]
            if 'proxy_stopcmd=' in line:
                line = line[:line.find("'") + 1] + 'true' + line[line.rfind("'"):]
        
            if 'dnsmasq_bind_port=' in line:
                line = line[:line.find("'") + 1] + str(initConfDect['dnsmasq_bind_port']) + line[line.rfind("'"):]
                        
            newConf += line
    #将修改后的内容写入文件
    with io.open(initConfDect['conf'], 'w', encoding='utf-8') as f:
        f.write(newConf)