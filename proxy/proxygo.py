import os, pycurl, sys, io,random
from tools import startProxy,queryProxyID,reStartProxy,obtainConfFolder,writeGoLog
from json import loads

workspace = os.path.split(os.path.realpath(__file__))[0]
weightFile =  os.path.join(workspace,'weight.temp')
subTemp = os.path.join(workspace,'sub.temp')
logFile = os.path.join(workspace,'proxygo.log')

google = 'www.google.com'
baidu = 'www.baidu.com'
tempConfig = ''
tempCounter = -1

def databack(buf):
    pass

def checkNet(url):
    if os.system('ping -c 1 {0}'.format(url)) == 0:
        return True
    else:
        return False

def checkNetFromConf(conf):
    with io.open(conf,'r', encoding='utf-8') as f:
        mDict = loads(f.read())
        return checkNet(mDict['server'])
    return False

def checkProxy(c):
    c.setopt(pycurl.URL, google)
    try:
        c.perform()
        c.close()
        return True
    except:
        return False

def obtainWeightDict(filePath):
    mDict = {}
    with io.open(filePath, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                w = line.replace('\n', '').split('|')
                mDict[w[1]] = int(w[0])
    return mDict

def addrPick(c, weightDict):
    global tempConfig,tempCounter
    #位置计数器
    counter = 0
    for w in weightDict:
        #取出能ping通的地址，从之前的那个地址开始
        if counter > tempCounter:
            #先检测能够连接到服务器
            if checkNetFromConf(os.path.join(confFolder, '{0}.json'.format(w.key))) == False:
                counter += 1
                continue
            else:
                tempCounter = counter
                tempConfig = w.key
        else:
            counter += 1
            continue
        #切换代理
        reStartProxy(os.path.join(confFolder, '{0}.json'.format(tempConfig)))
    if checkProxy(c) == True:
        #c已关闭
        #写日志
        #权重修改并写入文件
        weightDict[tempConfig] += 1
        with io.open(weightFile, 'w', encoding='utf-8') as f:
            for key,value in weightDict:
                f.write('{0}|{1}\n'.format(str(value), key))
        writeGoLog(logFile, 'INF: Change config:{0}'.format(tempConfig))
        sys.exit(0)
    else:
        #代理异常，重新挑选代理地址
        addrPick(c, weightDict)
    
    writeGoLog(logFile, 'ERR: No services available')
    sys.exit(0)


#先检测网络是否可用,不可用直接写日志退出
if checkNet(baidu) == False:
    writeGoLog(logFile, 'ERR: Request {} fail. Net maybe error'.format(baidu))
    sys.exit(0)


#检测代理是否开启，未开启则开启，找不到配置文件直接退出
if int(queryProxyID()) < 0:
    with io.open(weightFile, 'r', encoding='utf-8') as f:
        tempConfig = loads(f.read())['last']
        if len(tempConfig) > 0:
            startProxy(tempConfig['last'])
        else:
            writeGoLog(logFile, 'ERR: No config cache')
            sys.exit(0)

#pycurl
c = pycurl.Curl()
c.setopt(pycurl.WRITEFUNCTION, databack)

confFolder = obtainConfFolder(subTemp)
weightDict = sorted(obtainWeightDict(weightFile).items(),key=lambda x:x[1])

#检测代理可行性
if checkProxy(c) == True:
    #代理正常，此时是使用最后一次的配置或者正常检测进入
    #此时只需要记录检测时间以及状态即可，无需修改权重
    writeGoLog(logFile, 'INF: Proxy normally. Config:{0}'.format(tempConfig))
    sys.exit(0)
else:
    #代理异常，进入挑选代理地址
    addrPick(c, weightDict)



# print(google)
# print('HTTP响应状态:{}'.format(c.getinfo(pycurl.HTTP_CODE)))
# print('DNS解析时间:{}'.format(c.getinfo(pycurl.NAMELOOKUP_TIME)))
# print('建立连接时间:{}'.format(c.getinfo(pycurl.CONNECT_TIME)))
# print('准备传输时间:{}'.format(c.getinfo(pycurl.PRETRANSFER_TIME)))
# print('传输开始时间:{}'.format(c.getinfo(pycurl.STARTTRANSFER_TIME)))
# print('传输结束时间:{}'.format(c.getinfo(pycurl.TOTAL_TIME)))
# print('下载数据包大小:{}'.format(c.getinfo(pycurl.SIZE_DOWNLOAD)))
# print('HTTP头大小:{}'.format(c.getinfo(pycurl.HEADER_SIZE)))
# print('平均下载速度:{}'.format(c.getinfo(pycurl.SPEED_DOWNLOAD)/1024))

# 
# c.perform()
# print(baidu)
# print('HTTP响应状态:{}'.format(c.getinfo(pycurl.HTTP_CODE)))
# print('DNS解析时间:{}'.format(c.getinfo(pycurl.NAMELOOKUP_TIME)))
# print('建立连接时间:{}'.format(c.getinfo(pycurl.CONNECT_TIME)))
# print('准备传输时间:{}'.format(c.getinfo(pycurl.PRETRANSFER_TIME)))
# print('传输开始时间:{}'.format(c.getinfo(pycurl.STARTTRANSFER_TIME)))
# print('传输结束时间:{}'.format(c.getinfo(pycurl.TOTAL_TIME)))
# print('下载数据包大小:{}'.format(c.getinfo(pycurl.SIZE_DOWNLOAD)))
# print('HTTP头大小:{}'.format(c.getinfo(pycurl.HEADER_SIZE)))
# print('平均下载速度:{}'.format(c.getinfo(pycurl.SPEED_DOWNLOAD)/1024))




# c.close()

