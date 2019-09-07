import os
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from sail_widget.s_button import HelpButton
from sail_widget.tooltip import create_tooltip
from sail_widget.s_label import SLabel
from sail_widget.s_entry import SEntry
from sail_widget.s_button import SButton
from sail_widget.s_combobox import SCombbox
from sail_widget.s_checkbox import SCheckbutton

from tools.configer import Configer
from tools.text import *
from tools.check import Check
from tools.format_convertor import pdbqt_2_pdb
from tools.format_convertor import ob_join, ob, extract_pdbqt


# 复合
class Tab6(object):

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        # 需要保存的参数
        self.input_format = None
        self.complex_ligand_num_entry = None
        self.remain_ligand = None
        self.choose_ligands_entry = None
        self.choose_output_entry = None
        self.extract_output_entry = None

        self._choose_ligand_frame()
        self._choose_protein_frame()
        self._choose_output_frame()
        self._start_join()

        # 帮助按钮
        help_button = HelpButton(root=self.root, help_text=TAB6_HELP_TEXT, x=410, y=300, width=80)
        create_tooltip(help_button.help_button, "获取帮助")

    def _choose_ligand_frame(self):
        choose_ligand_labelframe = LabelFrame(self.root, text="选择/提取配体")
        choose_ligand_labelframe.place(x=10, y=10, width=570, height=120)

        # 选择输入配体的格式
        SLabel(root=choose_ligand_labelframe, text="输入格式：",
               x=10, y=0)
        input_format_text = ("pdbqt", "sdf", "pdb")
        self.input_format = SCombbox(root=choose_ligand_labelframe, textvariable=StringVar(),
                                     values=input_format_text,
                                     default_value=Configer.get_para("complex_ligand_format"),
                                     x=80, y=0, width=60)
        create_tooltip(self.input_format.combobox, "导入配体的格式")

        # 选择第几个配体
        SLabel(root=choose_ligand_labelframe, text="选择第",
               x=160, y=0)
        self.complex_ligand_num_entry = SEntry(choose_ligand_labelframe, textvariable=StringVar(),
                                               text=Configer.get_para("complex_ligand_num"),
                                               x=205, y=2, width=20)
        create_tooltip(self.complex_ligand_num_entry.entry, "只针对多构象pdbqt文件。输入"
                                                            "要进行复合或者提取的构象。"
                                                            "如果为0则全部提取/复合")
        SLabel(root=choose_ligand_labelframe, text="个构象",
               x=230, y=0)

        # 选择配体
        choose_ligands_button = SButton(choose_ligand_labelframe, text="选择单/多个配体", x=10, y=30)
        create_tooltip(choose_ligands_button.button, "选择一个或者多个所选格式的配体")
        choose_ligand_dir_button = SButton(choose_ligand_labelframe, text="选择文件夹", x=110, y=30)
        create_tooltip(choose_ligand_dir_button.button, "选择包含配体的文件夹，匹配其中所选格式的文件")
        self.choose_ligands_entry = SEntry(root=choose_ligand_labelframe, textvariable=StringVar(),
                                           text=Configer.get_para("choose_complex_ligands"),
                                           x=200, y=34, width=360)
        create_tooltip(self.choose_ligands_entry.entry, "所选的配体或者包含配体的目录")
        choose_ligands_button.bind_open_files(entry_text=self.choose_ligands_entry.textvariable,
                                              title="选择单/多个配体",
                                              file_type=self.input_format.textvariable)
        choose_ligand_dir_button.bind_open_dir(entry_text=self.choose_ligands_entry.textvariable,
                                               title="选择包含配体文件的文件夹")

        # 选择单独输出配体文件夹
        choose_output_button = SButton(choose_ligand_labelframe, text="提取配体输出路径", x=10, y=65)
        create_tooltip(choose_output_button.button, "单独提取配体，选择要输出的文件夹。")
        self.extract_output_entry = SEntry(choose_ligand_labelframe,
                                           textvariable=StringVar(),
                                           text=Configer.get_para("extract_pdbqt_dir"),
                                           x=120, y=65 + 3, width=340)
        create_tooltip(self.extract_output_entry.entry, "输出的文件夹")
        choose_output_button.bind_open_dir(entry_text=self.extract_output_entry.textvariable,
                                           title="选择提取配体输出的文件夹")
        extract_button = SButton(choose_ligand_labelframe, text="提取选定的配体",
                                 x=470, y=65)
        extract_button.button.bind("<Button-1>", self.extract)
        create_tooltip(extract_button.button, "提取配体")

    def _choose_protein_frame(self):
        choose_protein_labelframe = LabelFrame(self.root, text="选择受体")
        choose_protein_labelframe.place(x=10, y=135, width=570, height=50)

        choose_proteins = SButton(root=choose_protein_labelframe, text="选择受体", x=10, y=0)
        create_tooltip(choose_proteins.button, "选择pdbqt格式的受体")
        self.choose_proteins_entry = SEntry(root=choose_protein_labelframe, textvariable=StringVar(),
                                            text=Configer.get_para("choose_complex_proteins"),
                                            x=110, y=4, width=450)
        create_tooltip(self.choose_proteins_entry.entry, "受体文件")
        choose_proteins.bind_open_file(entry_text=self.choose_proteins_entry.textvariable,
                                       title="选择蛋白受体", file_type="pdbqt")

    def _choose_output_frame(self):
        choose_output_labelframe = LabelFrame(self.root, text="复合物输出")
        choose_output_labelframe.place(x=10, y=190, width=570, height=50)

        choose_output = SButton(root=choose_output_labelframe, text="选择输出文件夹", x=10, y=0)
        create_tooltip(choose_output.button, "选择复合物输出目录")
        self.choose_output_entry = SEntry(root=choose_output_labelframe, textvariable=StringVar(),
                                          text=Configer.get_para("choose_complex_output"),
                                          x=110, y=4, width=450)
        create_tooltip(self.choose_output_entry.entry, "所选的复合物输出目录")
        choose_output.bind_open_dir(entry_text=self.choose_output_entry.textvariable,
                                    title="选择复合物输出的文件夹")

    def _start_join(self):
        y = 250
        join_button = SButton(root=self.root, text="结合", x=10, y=y)
        create_tooltip(join_button.button, "将配体和受体结合成一个文件")
        join_button.button.bind("<Button-1>", self._join)

        self.progress = Progressbar(self.root, mode="determinate")
        self.progress.place(x=100, y=y + 2, width=400)
        create_tooltip(self.progress, "结合进度")

        self.progress_label = SLabel(self.root, text="没有任务", x=510, y=y)

        text_y = 286
        current_ligand_frame = Frame(self.root, width=400, height=40)
        current_ligand_frame.place(x=10, y=text_y)
        self.current_ligand = SLabel(root=current_ligand_frame, text="", x=0, y=0)

        # 是否保留提取配体
        self.remain_ligand = SCheckbutton(self.root
                                          , text="保留提取构象", variable=StringVar(),
                                          value=Configer.get_para("remain_ligand"),
                                          x=10, y=text_y + 20)
        create_tooltip(self.remain_ligand.checkbutton, "保留提取或者转换的构象。")

    def _join(self, event):
        input_format = self.input_format.textvariable.get()
        input_ligands_full = self.choose_ligands_entry.entry.get()
        input_receptor = self.choose_proteins_entry.entry.get()
        output_dir = self.choose_output_entry.entry.get()
        choose_num = self.complex_ligand_num_entry.entry.get()
        remain = self.remain_ligand.variable.get()

        # 所有选择的路径和文件都不能为空。
        if input_ligands_full == "" or input_receptor == "" or output_dir == "":
            messagebox.showerror("错误！", "输入不能为空！")
            return

        # 不能包括空格
        if Check.has_space(input_ligands_full):
            messagebox.showerror("错误！", "配体路径不能包含空格！")
            return
        if Check.has_space(input_receptor):
            messagebox.showerror("错误！", "受体路径不能包含空格！")
            return
        if Check.has_space(output_dir):
            messagebox.showerror("错误！", "输出路径不能包含空格！")
            return

        # 选择构象要是数字
        try:
            num = int(choose_num)
        except ValueError:
            messagebox.showerror("错误！", "提取的构象必须是数字！")
            return
        if num < 0:
            messagebox.showerror("错误！", "提取构象至少大于0！")
            return

        # 输出路径不存在则创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # 受体格式必须是pdbqt
        if not input_receptor.endswith(".pdbqt"):
            messagebox.showerror("错误！", "输入的受体必须是pdbqt格式。")
            return

        input_ligands = []

        # 输入的配体
        if input_ligands_full.endswith(";"):  # 如果是单个或者多个配体
            if input_ligands_full.split(".")[-1][0:-1] != input_format:  # 格式不匹配
                messagebox.showerror("错误！", "配体格式不是所选格式！")
                return
            input_ligands.extend(input_ligands_full.split(";")[0:-1])
        elif os.path.isdir(input_ligands_full):  # 如果选择的是目录
            list_file = os.listdir(input_ligands_full)
            for file in list_file:
                if file.endswith(input_format):
                    input_ligands.append(input_ligands_full + os.sep + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含%s格式的配体！" % input_format)
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        # 检查路径是否正确
        if not Check.check_python():
            return
        obabel_path = Configer.get_para("obabel_path")
        if not Check.check_obabel():
            return

        self.progress_label.label.configure(text="准备受体")
        self.progress_label.label.update()

        # 将受体pdbqt转成pdb
        input_pdb = output_dir + os.sep + input_receptor.split(".")[0].split(os.sep)[-1] + ".pdb"
        pdbqt_2_pdb(input_receptor, input_pdb)

        ligands = []

        self.progress_label.label.configure(text="准备配体")
        self.progress_label.label.update()

        if input_format == "pdbqt":
            for ligand in input_ligands:
                # 是否是单个配体:
                with open(ligand, "r") as f:
                    line = f.readline()
                    if "MODEL" not in line:
                        # 只有一个，直接转换成pdb
                        pdb_ligand = output_dir + os.sep + ligand.split(".")[0].split(os.sep)[-1] + ".pdb"
                        pdbqt_2_pdb(ligand, pdb_ligand)
                        ligands.append(pdb_ligand)
                    else:
                        output_pdbqts = extract_pdbqt(ligand, output_dir, num)
                        for output_pdbqt in output_pdbqts:
                            output_pdb = output_pdbqt[:-2]
                            pdbqt_2_pdb(output_pdbqt, output_pdb)
                            os.remove(output_pdbqt)
                            ligands.append(output_pdb)
        else:
            pdb_ligands = []
            # 全部转换成pdb格式
            for ligand in input_ligands:
                output_ligand = output_dir + os.sep + ligand.split(".")[0].split(os.sep)[-1] + ".pdb"
                ob(ligand, output_ligand)
                pdb_ligands.append(output_ligand)
            ligands = pdb_ligands

        # 进行复合
        self.progress["maximum"] = len(ligands)
        for ligand in ligands:
            # 更新进度条
            label_text = str(ligands.index(ligand) + 1) + os.sep + str(len(ligands))
            self.progress_label.label.configure(text=label_text)
            self.progress_label.label.update()

            self.progress["value"] = ligands.index(ligand) + 1
            self.progress.update()

            current_ligand = "当前配体：%s" % ligand.split(os.sep)[-1].split(".")[0]
            self.current_ligand.label.configure(text=current_ligand)
            self.current_ligand.label.update()

            output_name = ligand.split(os.sep)[-1].split(".")[0] + "_" + input_receptor.split(os.sep)[-1].split(".")[
                0] + ".pdb"
            output = output_dir + os.sep + output_name
            ob_join(ligand, input_pdb, output)

        # 如果不保留提取配体，删除提取配体
        if input_format == "pdbqt" and remain == "0":
            for ligand in ligands:
                os.remove(ligand)

        # 删除受体
        os.remove(input_pdb)

        messagebox.showinfo("成功！", "生成复合物成功！")
        self.progress_label.label.configure(text="没有任务")
        self.progress_label.label.update()

        self.progress["value"] = 0
        self.progress.update()

        self.current_ligand.label.configure(text="")
        self.current_ligand.label.update()

    def extract(self, event):
        input_format = self.input_format.textvariable.get()
        input_ligands_full = self.choose_ligands_entry.entry.get()
        output_dir = self.extract_output_entry.entry.get()
        choose_num = self.complex_ligand_num_entry.entry.get()

        # 所有选择的路径和文件都不能为空。
        if input_ligands_full == "" or output_dir == "":
            messagebox.showerror("错误！", "输入不能为空！")
            return

        # 不能包括空格
        if Check.has_space(input_ligands_full):
            messagebox.showerror("错误！", "配体路径不能包含空格！")
            return
        if Check.has_space(output_dir):
            messagebox.showerror("错误！", "输出路径不能包含空格！")
            return

        # 选择构象要是数字
        try:
            num = int(choose_num)
        except ValueError:
            messagebox.showerror("错误！", "提取的构象必须是数字！")
            return
        if num < 0:
            messagebox.showerror("错误！", "提取构象至少大于0！")
            return

        # 输出路径不存在则创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        input_ligands = []

        # 输入的配体
        if input_ligands_full.endswith(";"):  # 如果是单个或者多个配体
            if input_ligands_full.split(".")[-1][0:-1] != input_format:  # 格式不匹配
                messagebox.showerror("错误！", "配体格式不是所选格式！")
                return
            input_ligands.extend(input_ligands_full.split(";")[0:-1])
        elif os.path.isdir(input_ligands_full):  # 如果选择的是目录
            list_file = os.listdir(input_ligands_full)
            for file in list_file:
                if file.endswith(input_format):
                    input_ligands.append(input_ligands_full + os.sep + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含%s格式的配体！" % input_format)
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        for ligand in input_ligands:
            extract_pdbqt(ligand, output_dir, num)
        messagebox.showinfo("成功", "成功导入文件！")

    def save_para(self):
        self.config.para_dict["complex_ligand_format"] = self.input_format.textvariable.get()
        self.config.para_dict["complex_ligand_num"] = self.complex_ligand_num_entry.textvariable.get()
        self.config.para_dict["choose_complex_ligands"] = self.choose_ligands_entry.textvariable.get()
        self.config.para_dict["extract_pdbqt_dir"] = self.extract_output_entry.textvariable.get()
        self.config.para_dict["remain_ligand"] = self.remain_ligand.variable.get()
        self.config.para_dict["choose_complex_proteins"] = self.choose_proteins_entry.textvariable.get()
        self.config.para_dict["choose_complex_output"] = self.choose_output_entry.textvariable.get()
