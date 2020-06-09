#界面管理
from tkinter import LEFT, RIGHT, BOTTOM, BOTH, YES, TOP, X
from tkinter import Frame, Button, ttk, StringVar, Entry, Label

class SettingApp(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack(padx = 8, pady = 8)
        self.createWidgets()

    def createWidgets(self):
        self.kyara = StringVar()
        self.kyaraSel = ttk.Combobox(self, textvariable=self.kyara, state='readonly')
        self.kyaraSel.pack(side = LEFT, padx = 4, pady = 4)
        self.changeBtn = Button(self, text='Change', width=10)
        self.changeBtn.pack(side = RIGHT, padx = 4, pady = 4)