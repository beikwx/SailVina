from tkinter import *
from tkinter.ttk import *


class SLabel(object):
    def __init__(self, root, text, x, y, font=("微软雅黑", 10)):
        self.root = root
        self.text = text
        self.x = x
        self.y = y
        self.font = font

        self.label = Label(self.root, text=self.text, font=self.font)
        self.label.place(x=self.x, y=self.y)
