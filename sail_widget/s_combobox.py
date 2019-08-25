from tkinter.ttk import *


class SCombbox(object):

    def __init__(self, root, textvariable, values, default_value, x, y, width):
        self.root = root
        self.textvariable = textvariable
        self.values = values
        self.default_value = default_value
        self.x = x
        self.y = y
        self.width = width

        self.combobox = Combobox(self.root, textvariable=self.textvariable, state="readonly")
        self.combobox["values"] = self.values
        if self.default_value == "":
            self.textvariable.set(self.values[0])
        else:
            self.textvariable.set(self.default_value)
        self.combobox.place(x=self.x, y=self.y, width=self.width)
