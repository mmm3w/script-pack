import os

localAddr = '0.0.0.0'
localPort = 60080

#当前目录
workspace = os.path.split(os.path.realpath(__file__))[0]
#用于缓存一些数据的信息，json内容
infoCache = os.path.join(workspace,'info.cache')
#基础的ss-tproxy配置
initConf = os.path.join(workspace, 'init.json')
#检测日志
logFile = os.path.join(workspace,'kudzu.log')
#备选服务器权重
weightTemp = os.path.join(workspace,'weight.temp')
#服务器列表，用于选择服务器
listJson = 'list.json'

#用于检测网络连通性
localTest = 'myip.ipip.net'
#用于检测代理连通性
internTest = 'www.google.com'
#代理速度参照(Byte/s)
internRefer = 0

#备选地址过滤
alnatag = ('hk','jp')

startc = '(ssr-redir -c {0} -u </dev/null &>>/var/log/ssr-redir.log &)'
stopc = 'sudo kill -9 {0}'
statusc = 'sudo ss-tproxy status'
ssrpidc = 'sudo pidof ssr-redir'
curlspeedc = "curl -o /dev/null -s -w '%{speed_download}' {0}"
pingc = 'ping -c 1 {0}'
