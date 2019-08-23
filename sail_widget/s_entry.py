from tkinter import *


class SEntry(object):

    def __init__(self, root, text_variable, text, x, y, width):
        self.root = root
        self.x = x
        self.y = y
        self.width = width
        self.text_variable = text_variable
        self.text_variable.set(text)

        self.entry = Entry(self.root, textvariable=self.text_variable)
        self.entry.place(x=self.x, y=self.y, width=self.width)
