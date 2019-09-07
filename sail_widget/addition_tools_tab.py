from tkinter import messagebox
from tkinter import *

from sail_widget.s_button import HelpButton, SButton
from sail_widget.tooltip import create_tooltip
from sail_widget.s_toplevel import STopLevel
from sail_widget.s_entry import SEntry
from sail_widget.s_label import SLabel

from tools.text import *
from tools.configer import Configer
from tools.file_processor import gen_smi_der
from tools.check import Check


# 其他所有工具，全部以按钮来显示
class AdditionToolsTab(object):

    def __init__(self, tab, config: Configer):
        self.root = tab
        self.config = config

        # 需要保存的参数
        self.input_smi = ""
        self.output_path = ""

        self.input_smi_entry = None
        self.output_path_entry = None

        # 创建按钮
        self.create_buttons()

        # 帮助按钮
        help_button = HelpButton(root=self.root, help_text=TAB8_HELP_TEXT, x=410, y=300, width=80)
        create_tooltip(help_button.help_button, "获取帮助")

    def create_buttons(self):
        gen_smi_button = SButton(self.root, text="分子生成器", x=10, y=10)
        create_tooltip(gen_smi_button.button, "根据smi生成不同取代基衍生物")
        gen_smi_button.button.bind("<Button-1>", self.gen_smi)

    def gen_smi(self, event):
        windows = STopLevel(self.root, win_x=570, win_y=100, title="分子生成器").toplevel

        # 输入smi
        SLabel(windows, text="输入smi", x=10, y=10)
        self.input_smi_entry = SEntry(windows, textvariable=StringVar(),
                                      text=Configer.get_para("input_smi") if self.input_smi == "" else self.input_smi,
                                      x=80, y=13, width=470)
        create_tooltip(self.input_smi_entry.entry, "输入含有[R]的smi文本")

        # 输出目录
        output_button = SButton(windows, text="选择输出目录",
                                x=10, y=50)
        create_tooltip(output_button.button, "选择衍生物输出的目录")
        self.output_path_entry = SEntry(windows, textvariable=StringVar(),
                                        text=Configer.get_para(
                                            "mol_output_path") if self.output_path == "" else self.output_path,
                                        x=100, y=53, width=360)
        create_tooltip(self.output_path_entry.entry, "选择衍生物mol的输出目录")
        output_button.bind_open_dir(entry_text=self.output_path_entry.textvariable,
                                    title="选择衍生物输出目录", parent=windows)

        gen_button = SButton(windows, "生成衍生物",
                             x=465, y=50)
        create_tooltip(gen_button.button, "开始生成衍生物")
        gen_button.button.bind("<Button-1>", self._gen_smi)

        # 关闭窗口保存参数
        windows.protocol("WM_DELETE_WINDOW", lambda: self.save_smi(windows,
                                                                   self.input_smi_entry.textvariable.get(),
                                                                   self.output_path_entry.textvariable.get()))

    def _gen_smi(self, event):

        if not Check.check_obabel(Configer.get_para("obabel_path")):
            messagebox.showerror("错误！", "请检查obabel路径是否配置正确！")
            return

        smi = self.input_smi_entry.textvariable.get()
        output_path = self.output_path_entry.textvariable.get()

        if Check.check_path(output_path):
            messagebox.showerror("错误", "输出路径不能为空或者包含空格！")
            return

        # 如果只有一个元素则表示没有[R]标签
        if len(smi.split("[R]")) == 1:
            messagebox.showerror("错误", "%s没有[R]标签！" % smi)
            return

        gen_smi_der(smi, output_path)
        messagebox.showinfo("成功！", "成功生成衍生物！\n请检查后使用。")

    def save_smi(self, window: Toplevel, input_smi, output_path):
        self.input_smi = input_smi
        self.output_path = output_path
        window.destroy()

    def save_para(self):
        self.config.para_dict["input_smi"] = self.input_smi
        self.config.para_dict["mol_output_path"] = self.output_path
