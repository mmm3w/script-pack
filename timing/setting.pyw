#配置语音GUI
import tkinter as tk
from kanvoice import obtainVoiceList
from gui import SettingApp 
from os import path

workspace = path.split(path.realpath(__file__))[0]
voice_folder = path.join(workspace, "voice")

def saveKyara():
    if app.kyara.get():
        confFile = open(path.join(workspace, 'voice.conf'), 'w+', encoding='utf-8')
        confFile.write(app.kyara.get())
        confFile.close()
    else:
        pass

root = tk.Tk()
app = SettingApp(root)
app.master.title('Setting')
app.pack(side = "top", fill = "both", expand = True)
app.kyaraSel['value'] = obtainVoiceList(voice_folder)
app.changeBtn['command'] = saveKyara

if path.exists(path.join(workspace, 'voice.conf')):
    per = open(path.join(workspace, 'voice.conf'), 'r', encoding='utf-8')
    app.kyara.set(per.read())
    per.close()

root.mainloop()