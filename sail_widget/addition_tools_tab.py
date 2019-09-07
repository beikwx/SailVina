from tkinter import messagebox
from tkinter import *

import os

from sail_widget.s_button import HelpButton, SButton
from sail_widget.tooltip import create_tooltip
from sail_widget.s_toplevel import STopLevel, SMultiTopLevel
from sail_widget.s_entry import SEntry
from sail_widget.s_label import SLabel
from sail_widget.s_combobox import SCombbox

from tools.text import *
from tools.configer import Configer
from tools.file_processor import gen_smi_der
from tools.check import Check
from tools.rmsd import charnley_cal_rmsd


# 其他所有工具，全部以按钮来显示
class AdditionToolsTab(object):

    def __init__(self, tab, config: Configer):
        self.root = tab
        self.config = config

        self.windows = None

        # 需要保存的参数
        self.input_smi = ""
        self.output_path = ""

        self.single_ligand = ""
        self.sec_ligands = ""
        self.rotate_method = ""
        self.reorder_method = ""

        # 需要保存的输入框
        self.input_smi_entry = None
        self.output_path_entry = None

        self.single_ligand_entry = None
        self.sec_ligands_entry = None
        self.rotate_method_box = None
        self.reorder_method_box = None

        # 创建按钮
        self.create_buttons()

        # 帮助按钮
        help_button = HelpButton(root=self.root, help_text=TAB8_HELP_TEXT, x=410, y=300, width=80)
        create_tooltip(help_button.help_button, "获取帮助")

    def create_buttons(self):
        gen_smi_button = SButton(self.root, text="分子生成器", x=10, y=10)
        create_tooltip(gen_smi_button.button, "根据smi生成不同取代基衍生物")
        gen_smi_button.button.bind("<Button-1>", self.gen_smi)

        cal_rmsd_button = SButton(self.root, text="计算小分子RMSD", x=110, y=10)
        create_tooltip(cal_rmsd_button.button, "计算两个小分子之间的RMSD值。")
        cal_rmsd_button.button.bind("<Button-1>", self.cal_rmsd)

    def gen_smi(self, event):
        self.windows = STopLevel(self.root, win_x=570, win_y=100, title="分子生成器").toplevel

        # 输入smi
        SLabel(self.windows, text="输入smi", x=10, y=10)
        self.input_smi_entry = SEntry(self.windows, textvariable=StringVar(),
                                      text=Configer.get_para("input_smi") if self.input_smi == "" else self.input_smi,
                                      x=80, y=13, width=470)
        create_tooltip(self.input_smi_entry.entry, "输入含有[R]的smi文本")

        # 输出目录
        output_button = SButton(self.windows, text="选择输出目录",
                                x=10, y=50)
        create_tooltip(output_button.button, "选择衍生物输出的目录")
        self.output_path_entry = SEntry(self.windows, textvariable=StringVar(),
                                        text=Configer.get_para(
                                            "mol_output_path") if self.output_path == "" else self.output_path,
                                        x=100, y=53, width=360)
        create_tooltip(self.output_path_entry.entry, "选择衍生物mol的输出目录")
        output_button.bind_open_dir(entry_text=self.output_path_entry.textvariable,
                                    title="选择衍生物输出目录", parent=self.windows)

        gen_button = SButton(self.windows, "生成衍生物",
                             x=465, y=50)
        create_tooltip(gen_button.button, "开始生成衍生物")
        gen_button.button.bind("<Button-1>", self._gen_smi)

        # 关闭窗口保存参数
        self.windows.protocol("WM_DELETE_WINDOW", lambda: self.save_smi(self.windows,
                                                                        self.input_smi_entry.textvariable.get(),
                                                                        self.output_path_entry.textvariable.get()))

    def _gen_smi(self, event):

        if not Check.check_obabel():
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

    def cal_rmsd(self, event):
        self.windows = STopLevel(self.root, win_x=570, win_y=130, title="计算RMSD").toplevel

        # 参考配体
        single_ligand_button = SButton(self.windows, text="选择参考配体", x=10, y=10)
        create_tooltip(single_ligand_button.button, "选择一个参考配体，只支持xyz格式")
        self.single_ligand_entry = SEntry(self.windows, textvariable=StringVar(),
                                          text=Configer.get_para(
                                              "single_ligand") if self.single_ligand == "" else self.single_ligand,
                                          x=100, y=13, width=450)
        create_tooltip(self.single_ligand_entry.entry, "选择的参考配体")
        single_ligand_button.bind_open_file(entry_text=self.single_ligand_entry.textvariable,
                                            title="选择参考配体",
                                            file_type="xyz",
                                            parent=self.windows)

        # 比较配体
        sec_ligand_button = SButton(self.windows, text="选择第二个配体",
                                    x=10, y=50)
        create_tooltip(sec_ligand_button.button, "选择需要比较的单个配体")
        sec_ligands_button = SButton(self.windows, text="选择文件夹", x=110, y=50)
        create_tooltip(sec_ligands_button.button, "选择第二个配体所在的文件夹")

        self.sec_ligands_entry = SEntry(self.windows, textvariable=StringVar(),
                                        text=Configer.get_para(
                                            "sec_ligands") if self.sec_ligands == "" else self.sec_ligands,
                                        x=200, y=53, width=350)
        create_tooltip(self.sec_ligands_entry.entry, "选择需要比较的配体")
        sec_ligand_button.bind_open_file(entry_text=self.sec_ligands_entry.textvariable,
                                         title="选择需要比较的配体",
                                         file_type="xyz",
                                         parent=self.windows)
        sec_ligands_button.bind_open_dir(entry_text=self.sec_ligands_entry.textvariable,
                                         title="选择需要比较的配体所在的文件夹", parent=self.windows)

        SLabel(root=self.windows, text="旋转方法", x=10, y=90)
        rotate_method_text = ("none", "kabsch", "quaternion")
        self.rotate_method_box = SCombbox(root=self.windows, textvariable=StringVar(),
                                          values=rotate_method_text,
                                          default_value=Configer.get_para(
                                              "rotate_method") if self.rotate_method == "" else self.rotate_method,
                                          x=70, y=90, width=85)
        create_tooltip(self.rotate_method_box.combobox, "是否旋转原子和旋转方法")

        SLabel(root=self.windows, text="原子对齐方法", x=170, y=90)
        reorder_method_text = ("hungarian", "distance")
        self.reorder_method_box = SCombbox(root=self.windows, textvariable=StringVar(),
                                           values=reorder_method_text,
                                           default_value=Configer.get_para(
                                               "reorder_method") if self.reorder_method == "" else self.reorder_method,
                                           x=260, y=90, width=85)
        create_tooltip(self.rotate_method_box.combobox, "是否旋转原子和旋转方法")

        rmsd_button = SButton(self.windows, "计算RMSD",
                              x=465, y=90)
        create_tooltip(rmsd_button.button, "计算RMSD")
        rmsd_button.button.bind("<Button-1>", self._cal_rmsd)

        # 关闭窗口保存参数
        self.windows.protocol("WM_DELETE_WINDOW", lambda: self.save_rmsd(self.windows,
                                                                         self.single_ligand_entry.textvariable.get(),
                                                                         self.sec_ligands_entry.textvariable.get(),
                                                                         self.rotate_method_box.textvariable.get(),
                                                                         self.reorder_method_box.textvariable.get()))

    def _cal_rmsd(self, event):
        single_ligand = self.single_ligand_entry.textvariable.get()
        sec_ligands = self.sec_ligands_entry.textvariable.get()
        rotate_method = self.rotate_method_box.textvariable.get()
        reorder_method = self.reorder_method_box.textvariable.get()

        if Check.check_path(single_ligand) or Check.check_path(sec_ligands):
            messagebox.showerror("错误", "选择的文件或者路径不能为空或者包括空格！")
            return

        if not Check.check_obabel():
            messagebox.showerror("错误！", "Obabel配置不正确!")
            return

        sec_ligands_path = []
        # 如果选择的是一个文件
        if os.path.isfile(sec_ligands):
            sec_ligands_path.append(sec_ligands)
        # 如果选的是多个文件
        elif os.path.isdir(sec_ligands):
            list_file = os.listdir(sec_ligands)
            for file in list_file:
                if file.endswith("xyz"):
                    sec_ligands_path.append(sec_ligands + os.sep + file)
            if len(sec_ligands_path) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含xyz的配体！")
                return
        else:
            messagebox.showerror("错误！请检查输入的配体！")
            return

        rmsds = {}

        for sec_ligand_path in sec_ligands_path:
            rmsd = charnley_cal_rmsd(single_ligand, sec_ligand_path,
                                     rotate_method, reorder_method)
            if rmsd:
                rmsds[os.path.split(sec_ligand_path)[-1][:-4]] = rmsd
            else:
                print("%s无法计算RMSD！" % sec_ligand_path)
                continue

        if len(rmsds) == 1:
            top = SMultiTopLevel(self.windows, win_x=400, win_y=100, title="RMSD结果").toplevel
            for ligand in rmsds:
                text = "%s    vs    %s" % (os.path.split(single_ligand)[-1],
                                           os.path.split(ligand)[-1])
                SLabel(top, text=text, x=10, y=10)
                text = rmsds[ligand]
                SLabel(top, text=text, x=10, y=50)
        elif len(rmsds) == 0:
            messagebox.showerror("错误！", "没有得到RMSD值！")
            return
        else:
            # 多个输出文件到目录中
            output_filename = os.path.join(sec_ligands, "rmsd.txt")
            with open(output_filename, "w") as f:
                f.writelines("second_ligand\trmsd\n")
                for ligand in rmsds:
                    f.write("%s\t%s\n" % (ligand, rmsds[ligand]))
            messagebox.showinfo("成功！", "成功导出rmsd结果到%s" % output_filename)

    def save_rmsd(self, window: Toplevel, singe_ligand, sec_ligands, rotate_method, reorder_method):
        self.single_ligand = singe_ligand
        self.sec_ligands = sec_ligands
        self.rotate_method = rotate_method
        self.reorder_method = reorder_method
        window.destroy()

    def save_para(self):
        self.config.para_dict["input_smi"] = self.input_smi
        self.config.para_dict["mol_output_path"] = self.output_path
        self.config.para_dict["single_ligand"] = self.single_ligand
        self.config.para_dict["sec_ligands"] = self.sec_ligands
        self.config.para_dict["rotate_method"] = self.rotate_method
        self.config.para_dict["reorder_method"] = self.reorder_method
