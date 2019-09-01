from tkinter import *
from tkinter.ttk import *

from sail_widget.s_button import HelpButton
from sail_widget.tooltip import create_tooltip


# 其他所有工具，全部以按钮来显示
class AdditionToolsTab(object):

    def __init__(self, tab, config):
        self.root = tab
        self.config = config
