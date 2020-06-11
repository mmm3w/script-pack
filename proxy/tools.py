import os,subprocess,io,time

def queryProxyID():
    with os.popen('pidof ssr-redir') as p:
        pid = p.read()
        if len(pid) != 0:
            return pid
        else:
            return -1

def closeProxy(pid = queryProxyID()):
    if pid > 0:
        os.system('sudo kill -9 {0}'.format(pid))
        print('Stop proxy process')

def startProxy(ssrConfigPath):
    if subprocess.run('ssr-redir -c {0} -u </dev/null &>>/var/log/ssr-redir.log &'.format(ssrConfigPath), stdout = subprocess.DEVNULL).returncode == 0:
        print('Start proxy process')

def reStartProxy(ssrConfigPath):
    closeProxy()
    startProxy(ssrConfigPath)

def obtainConfFolder(subTempPath):
    path = ''
    with io.open(subTempPath, 'r', encoding='utf-8') as f:
        path = f.readline().replace('\n','')
    return path

def writeGoLog(logPath, text):
    with io.open(logPath, 'a+', encoding='utf-8') as f:
        f.write('{0}\t|\t{1}\n'.format(time.asctime(time.localtime(time.time())),text))