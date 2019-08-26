from tkinter import *
from tkinter.ttk import *

from tools.text import *


class Tab7(object):

    def __init__(self, tab):
        self.label1 = Label(tab, text=TAB7_HELP_TEXT, wraplength=565)
        self.label1.place(x=10, y=10)
