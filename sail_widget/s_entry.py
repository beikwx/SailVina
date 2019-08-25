from tkinter import *


class SEntry(object):

    def __init__(self, root, textvariable, text, x, y, width):
        self.root = root
        self.x = x
        self.y = y
        self.width = width
        self.textvariable = textvariable
        self.textvariable.set(text)

        self.entry = Entry(self.root, textvariable=self.textvariable)
        self.entry.place(x=self.x, y=self.y, width=self.width)
