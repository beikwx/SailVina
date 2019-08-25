from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from sail_widget.tooltip import create_tooltip

from tools.s_file import *


class SButton(object):
    def __init__(self, root, text, x, y):
        self.root = root
        self.text = text
        self.x = x
        self.y = y

        self.button = Button(self.root, text=self.text)
        self.button.place(x=self.x, y=self.y)

        self.entry_text = None
        self.initial_dir = None
        self.title = None
        self.file_type = None
        self.parent = None

    def _bind_open_file(self, event):
        self.initial_dir = self.entry_text.get()
        filename = SFile().open_file(self.initial_dir, self.title, self.file_type, parent=self.parent)
        self.entry_text.set(filename)

    def bind_open_file(self, entry_text: str, title: str, file_type: str, parent=""):
        """
        给按钮绑定打开一个文件
        :param entry_text: 打开后初始位置
        :param title: 标题
        :param file_type: 要打开的文件类型
        :param parent: 在哪个控件上面显示，默认主窗口上
        """
        self.entry_text = entry_text
        self.title = title
        self.file_type = file_type
        self.parent = parent
        self.button.bind("<Button-1>", self._bind_open_file)

    def _bind_open_dir(self, event):
        self.initial_dir = self.entry_text.get()
        dir_name = SFile().open_dir(initial_dir=self.initial_dir, title=self.title)
        self.entry_text.set(dir_name)

    def bind_open_dir(self, entry_text: str, title: str):
        """
        给按钮绑定选择一个目录
        :param entry_text: 打开后初始位置
        :param title: 标题
        """
        self.entry_text = entry_text
        self.title = title
        self.button.bind("<Button-1>", self._bind_open_dir)

    def _bind_open_files(self, event):
        self.initial_dir = self.entry_text.get()
        try:
            file_type = self.file_type.get()
        except AttributeError:
            file_type = self.file_type
        self.filename_text = SFile().open_files(initial_dir=self.initial_dir, title=self.title,
                                                file_type=file_type)
        self.entry_text.set(self.filename_text)

    def bind_open_files(self, entry_text, title, file_type):
        self.entry_text = entry_text
        self.title = title
        self.file_type = file_type
        self.button.bind("<Button-1>", self._bind_open_files)


class HelpButton(object):

    def __init__(self, root, help_text, x, y, width):
        """

        :param root: 要放置到哪里
        :param help_text: 弹出提示框显示的文字
        :param x: 位置x
        :param y: 位置y
        :param width: 按钮宽度
        """
        self.root = root
        self.help_text = help_text
        self.x = x
        self.y = y
        self.width = width

        self.help_button = Button(self.root, text="帮助", command=self.show_help)
        create_tooltip(self.help_button, "获取帮助")
        self.help_button.place(x=self.x, y=self.y, width=self.width)

    def show_help(self):
        messagebox.showinfo("帮助", self.help_text)
