from time import time, localtime, asctime
from os import path
from json import loads
import sys, requests
from re import search,findall
import tkinter as tk
from tkinter import messagebox

workspace = path.split(path.realpath(__file__))[0]
logFilePath = path.join(workspace, 'paofu.log')
configFilePath = path.join(workspace, 'paofu.conf')

logFile = open(logFilePath, 'a+',  encoding='utf-8')

################################################################
def writeLog(title, str, isFinish):
    global logFile
    logFile.write('{0}\t|\t{1}\t|\t{2}\n'.format(title, asctime(localtime(time())),str))
    if isFinish:
        logFile.close()
        sys.exit()
################################################################

root = tk.Tk()
root.withdraw()

if not path.exists(configFilePath):
    writeLog('Error', 'Not find config file!', True)

try:
    configFile = open(configFilePath, 'r', encoding='utf-8')
    configDect = loads(configFile.read())
    configFile.close()
except:
    writeLog('Error', 'Config file parse error!', True)

loginUrl = configDect['url'] + '/auth/login'
userUrl = configDect['url'] + "/user"
checkinUrl = userUrl + "/checkin"
s = requests.session()

try:
    loginRes = s.post(loginUrl, data = {'email':configDect['mail'], 'passwd':configDect['pw']})
    writeLog('Login', loginRes.content.decode('unicode_escape'), False)
except:
    writeLog('Error', 'Login fail!', True)

try:
    checkinRes = s.post(checkinUrl)
    checkinStr = checkinRes.content.decode('unicode_escape')
    msgDect = loads(checkinStr)
    writeLog('Checkin', checkinStr, False)
except:
    writeLog('Error', 'Checkin fail!', False)

try:
    userRes = s.get(userUrl)
    userData = userRes.content.decode('utf-8')
    trafficNode = search(r'(?<=trafficDountChat\().*?(?=\))', userData.replace('\n', '').replace('\t', '').replace(' ','')).group(0).replace("'", '').split(',')
    writeLog('Traffic', '已用:{0}  可用:{1}'.format(trafficNode[0], trafficNode[2]), False)
except:
    writeLog('Error', 'Query traffic fail!', False)

try:
    messagebox.showinfo('Hint', '{}'.format(msgDect['msg']))
except:
    pass