import tkinter
import json
from tkinter import *

import foodproducts.foodproduct
from foodproducts.foodproduct import *


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
        self.clientModeButton.bind('<Button-1>', foodproducts.foodproduct.writeproduct('Котлета из говядины',26.11,11.75,0.0,217,100,40))

        self.adminModeButton = Button(self.modeSelector)
        self.adminModeButton.configure(text='Администратор')
        self.adminModeButton.pack(side=LEFT)

    def getclientgui(self, event) -> None:
        self.parent.destroy()