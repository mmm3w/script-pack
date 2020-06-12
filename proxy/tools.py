import os,io,time


def writeText(workspace, fileName, text):
    with io.open(os.path.join(workspace,fileName), 'w', encoding = 'utf-8') as f:
        f.write(text)

def writeGoLog(logPath, text):
    with io.open(logPath, 'a+', encoding='utf-8') as f:
        f.write('{0}\t{1}\n'.format(time.asctime(time.localtime(time.time())),text))

###########################################################################

def queryProxyID():
    return -1
    # with os.popen('pidof ssr-redir') as p:
    #     pid = p.read()
    #     if len(pid) != 0:
    #         return pid
    #     else:
    #         return -1

def closeProxy(pid = queryProxyID()):
    if int(pid) > 0:
        os.system('sudo kill -9 {0}'.format(pid))
        print('Stop proxy process')

def startProxy(ssrConfigPath):
    if os.system('ssr-redir -c {0} -u </dev/null &>>/var/log/ssr-redir.log &'.format(ssrConfigPath)) == 0:
        print('Start proxy process')

def reStartProxy(ssrConfigPath):
    closeProxy()
    startProxy(ssrConfigPath)

def obtainConfFolder(subTempPath):
    path = ''
    with io.open(subTempPath, 'r', encoding='utf-8') as f:
        path = f.readline().replace('\n','')
    return path

