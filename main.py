import tkinter
from tkinter import *


class WelcomeMenuEnter:
    def getclientgui(self) -> None:
        enterMenu.destroy()

    def __init__(self, parent):
        self.modeSelector = Frame(enterMenu)
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


enterMenu = Tk()
enterMenu.title('Выберите пользователя')
enterMenu.maxsize(600, 300)
enterMenu.minsize(600, 300)
enterMenu.resizable(None, None)
welcomeMenu = WelcomeMenuEnter(enterMenu)
enterMenu.mainloop()



