import os

localAddr = '0.0.0.0'
localPort = 60080

#当前目录
workspace = os.path.split(os.path.realpath(__file__))[0]
#用于缓存一些数据的信息，json内容
infoCache = os.path.join(workspace,'info.cache')
#基础的ss-tproxy配置
initConf = os.path.join(workspace, 'init.json')
#服务器列表，用于选择服务器
listJson = 'list.json'


startc = '(ssr-redir -c {0} -u </dev/null &>>/var/log/ssr-redir.log &)'
stopc = 'sudo kill -9 {0}'
statusc = 'sudo ss-tproxy status'
ssrpids = 'sudo pidof ssr-redir'