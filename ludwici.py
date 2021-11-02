import tkinter
from tkinter import *


class WelcomeMenuEnter:

    def __init__(self, parent):
        self.parent = parent

        self.modeSelector = Frame(parent)
        self.modeSelector.pack()

        self.welcomeMessage = tkinter.Label()
        self.welcomeMessage['text'] = 'Добро пожаловать в службу заказа еды'
        self.welcomeMessage.pack()

        self.clientModeButton = Button(self.modeSelector)
        self.clientModeButton.configure(text='Клиент')
        self.clientModeButton.pack(side=LEFT)
        self.clientModeButton.bind('<Button-1>', self.getclientgui)

        self.adminModeButton = Button(self.modeSelector)
        self.adminModeButton.configure(text='Администратор')
        self.adminModeButton.pack(side=LEFT)

    def getclientgui(self, event) -> None:
        self.parent.destroy()