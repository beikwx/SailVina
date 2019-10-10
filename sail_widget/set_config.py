from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from sail_widget.s_button import SButton
from sail_widget.s_entry import SEntry
from sail_widget.tooltip import create_tooltip
from sail_widget.s_toplevel import STopLevel

from tools.check import Check
from tools.file_path import *
from tools.configer import Configer


class SetConfig(object):

    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.top = STopLevel(self.root, 400, 130, "设置参数").toplevel

        self.choose_python_path_entry = None
        self.choose_obabel_path_entry = None

        self.choose_python()
        self.choose_obabel()
        self.yesorno()

    def choose_python(self):
        y = 10
        # python路径
        choose_python_path = SButton(self.top,
                                     text="选择ADT的python路径",
                                     x=10, y=y)
        create_tooltip(choose_python_path.button, "必须选择mgltools目录里面的python.exe文件！\n"
                                                  "比如：\nC:/mgltools/python.exe")
        self.choose_python_path_entry = SEntry(root=self.top,
                                               textvariable=StringVar(),
                                               text=Configer.get_para("python_path"),
                                               x=150, y=y + 4, width=230)
        create_tooltip(self.choose_python_path_entry.entry, "ADT的python路径")
        choose_python_path.bind_open_file(entry_text=self.choose_python_path_entry.textvariable,
                                          title="选择ADT中的python.exe",
                                          file_type="exe", parent=self.top)

    def choose_obabel(self):
        y = 50  # python路径
        choose_obabel_path = SButton(self.top,
                                     text="选择obabel.exe的路径",
                                     x=10, y=y)
        create_tooltip(choose_obabel_path.button, "选择obabel.exe文件")
        self.choose_obabel_path_entry = SEntry(root=self.top,
                                               textvariable=StringVar(),
                                               text=Configer.get_para("obabel_path"),
                                               x=150, y=y + 4, width=230)
        create_tooltip(self.choose_obabel_path_entry.entry, "obabel.exe位置")
        choose_obabel_path.bind_open_file(entry_text=self.choose_obabel_path_entry.textvariable,
                                          title="选择obabel.exe",
                                          file_type="exe", parent=self.top)

    def yesorno(self):
        y = 90
        ok_but = Button(self.top, text="确定", command=self.save_para)
        ok_but.place(x=200, y=y)
        cancel_btn = Button(self.top, text="取消", command=self.top.destroy)
        cancel_btn.place(x=300, y=y)

        self.top.protocol("WM_DELETE_WINDOW", self.ask_save_para)

    def save_para(self):
        # 检查python
        choose_python_path = self.choose_python_path_entry.textvariable.get()
        if not Check.check_python(choose_python_path):
            choose_python_path = ""

        # 检查obabel
        obabel_path = self.choose_obabel_path_entry.textvariable.get()
        if not Check.check_obabel(obabel_path):
            obabel_path = ""

        self.config.para_dict["python_path"] = choose_python_path
        self.config.para_dict["obabel_path"] = obabel_path
        # 读取原始的配置文件
        with open(para_file, "r") as f:
            for line in f.readlines():
                key = line.split("=")[0]
                if key == "python_path" or key == "obabel_path":
                    continue
                try:
                    value = line.split("=")[1]
                except IndexError:
                    value = ""
                self.config.para_dict[key] = value.strip()

        self.config.save_para()
        self.top.destroy()

    def ask_save_para(self):
        if messagebox.askokcancel("退出", "保存参数？"):
            self.save_para()
