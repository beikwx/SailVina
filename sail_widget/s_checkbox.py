from tkinter.ttk import *


class SCheckbutton(object):

    def __init__(self, root, text, variable, value, x, y):
        self.root = root
        self.text = text
        self.variable = variable
        self.value = value if value != "" else 0
        self.x = x
        self.y = y

        self.checkbutton = Checkbutton(self.root, text=self.text, variable=self.variable)
        self.variable.set(value)
        self.checkbutton.place(x=self.x, y=self.y)
