import tkinter
from tkinter import *

from ludwici import WelcomeMenuEnter

enterMenu = Tk()
enterMenu.title('Выберите пользователя')
enterMenu.maxsize(600, 300)
enterMenu.minsize(600, 300)
enterMenu.resizable(None, None)
welcomeMenu = WelcomeMenuEnter(enterMenu)
enterMenu.mainloop()
print('спасибо за гит ludwici')



