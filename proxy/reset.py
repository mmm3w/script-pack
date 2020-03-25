import os, io, sys
from json import loads

def readJson2Dict(path):
    jsonFile = io.open(path, 'r', encoding='utf-8')
    jsonFileStr = jsonFile.read()
    jsonFile.close()
    return loads(jsonFileStr)

subDict = readJson2Dict('subscription.json')

sLDict = readJson2Dict(os.path.join(subDict['list'], 'ServerList.json'))

mark = 0
for key, value in sLDict.items():
    mark = mark + 1
    print('[{0}]\t{1}'.format(mark, value))

number = int(input('Select server:'))

mark = 0
for key, value in sLDict.items():
    mark = mark + 1
    if mark == number:
        ssrConfigPath = os.path.join(subDict['folder'], '{}.json'.format(key))

if 'ssrConfigPath' not in dir():
    print("Error number")
    sys.exit(0)

ssrDict = readJson2Dict(ssrConfigPath)
proxyconfDict = readJson2Dict('proxy.json')

proxyconfDict['proxy_svraddr4'] = "({})".format(ssrDict['server'])
proxyconfDict['proxy_svrport'] = ssrDict['server_port']
proxyconfDict['proxy_startcmd'] = "(ssr-redir -c {} -u </dev/null &>>/var/log/ssr-redir.log &)".format(ssrConfigPath)

spList = ['proxy_svraddr4','proxy_svraddr6','dnsmasq_conf_dir','dnsmasq_conf_file','dnsmasq_conf_string','chinadns_privaddr4','chinadns_privaddr6']


tproxyConfig = io.open(proxyconfDict['config'], 'w', encoding='utf-8')
for key, value in proxyconfDict.items():
    if key == 'config':
        continue
    if key in spList:
        if isinstance(value, bool):
            tproxyConfig.write("{0}={1}\n".format(key, value).lower())
        else:
            tproxyConfig.write("{0}={1}\n".format(key, value))
    else:
        if isinstance(value, bool):
            tproxyConfig.write("{0}='{1}'\n".format(key, value).lower())
        else:
            tproxyConfig.write("{0}='{1}'\n".format(key, value))

tproxyConfig.close()   




