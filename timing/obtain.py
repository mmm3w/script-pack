#下载语音GUI
import tkinter as tk
from os import path

from kanvoice import requestVoiceFileFromKanWiki

workspace = path.split(path.realpath(__file__))[0]
url = input('Input url:')
nameKan = input('Input name:')
requestVoiceFileFromKanWiki(url, workspace, nameKan)