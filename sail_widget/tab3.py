import shutil

from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from sail_widget.s_button import HelpButton
from sail_widget.tooltip import create_tooltip
from sail_widget.s_label import SLabel
from sail_widget.s_entry import SEntry
from sail_widget.s_button import SButton
from sail_widget.s_checkbox import SCheckbutton
from sail_widget.s_combobox import SCombbox

from tools.text import *
from tools.check import Check
from tools.format_convertor import *
from tools.file_processor import mk_output_dir


# 准备配体
class Tab3(object):

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        # 需要保存的参数
        self.input_format = None
        self.choose_ligands_entry = None

        self.output_format = None
        self.gen3d = None
        self.ph = None
        self.is_minimize = None

        self.choose_output_dir_entry = None

        self._create_choose_ligand_frame()
        self._create_output_ligand_frame()

        # 开始转换
        self._create_convert()

        # 帮助按钮
        help_button = HelpButton(root=self.root, help_text=TAB3_HELP_TEXT, x=410, y=300, width=80)
        create_tooltip(help_button.help_button, "获取帮助")

    def _create_choose_ligand_frame(self):
        choose_ligand_labelframe = LabelFrame(self.root, text="输入选项")
        choose_ligand_labelframe.place(x=10, y=10, width=570, height=85)

        # 选择输入配体的格式
        SLabel(root=choose_ligand_labelframe, text="输入格式：",
               x=10, y=0)
        input_format_text = ("mol", "sdf", "mol2", "pdb", "pdbqt", "xyz")
        self.input_format = SCombbox(root=choose_ligand_labelframe, textvariable=StringVar(),
                                     values=input_format_text,
                                     default_value=Configer.get_para("input_format"),
                                     x=80, y=0, width=60)
        create_tooltip(self.input_format.combobox, "导入配体的格式")

        choose_ligands_button = SButton(choose_ligand_labelframe, text="选择单/多个配体", x=10, y=30)
        create_tooltip(choose_ligands_button.button, "选择一个或者多个所选格式的配体")
        choose_ligand_dir_button = SButton(choose_ligand_labelframe, text="选择文件夹", x=110, y=30)
        create_tooltip(choose_ligand_dir_button.button, "选择包含配体的文件夹，匹配其中所选格式的文件")
        self.choose_ligands_entry = SEntry(root=choose_ligand_labelframe, textvariable=StringVar(),
                                           text=Configer.get_para("choose_ligands"),
                                           x=200, y=34, width=360)
        create_tooltip(self.choose_ligands_entry.entry, "所选的配体或者包含配体的目录")
        choose_ligands_button.bind_open_files(entry_text=self.choose_ligands_entry.textvariable,
                                              title="选择单/多个配体",
                                              file_type=self.input_format.textvariable)
        choose_ligand_dir_button.bind_open_dir(entry_text=self.choose_ligands_entry.textvariable,
                                               title="选择包含配体文件的文件夹")

    def _create_output_ligand_frame(self):
        choose_output_ligand_labelframe = LabelFrame(self.root, text="输出选项")
        choose_output_ligand_labelframe.place(x=10, y=100, width=570, height=115)

        # 第一排
        first_y = 0
        SLabel(root=choose_output_ligand_labelframe, text="输出格式：", x=10, y=first_y)
        output_format_text = ("pdbqt", "pdb", "sdf", "xyz")
        self.output_format = SCombbox(root=choose_output_ligand_labelframe, textvariable=StringVar(),
                                      values=output_format_text,
                                      default_value=Configer.get_para("output_format"),
                                      x=80, y=0, width=60)
        create_tooltip(self.output_format.combobox, "导出配体的格式")

        # 第二排
        second_y = 30
        # 生成3d
        SLabel(root=choose_output_ligand_labelframe, text="选      项：", x=10, y=second_y)
        self.gen3d = SCheckbutton(root=choose_output_ligand_labelframe, text="3d", variable=StringVar(),
                                  value=Configer.get_para("gen3d"), x=150, y=second_y)
        create_tooltip(self.gen3d.checkbutton, "是否生成三维坐标。\n"
                                               "输入配体是平面结构时，请勾选。\n"
                                               "输入配体时立体结构时，不建议勾选。")

        # pH
        SLabel(root=choose_output_ligand_labelframe, text="pH", x=80, y=second_y)
        self.ph = SEntry(root=choose_output_ligand_labelframe, textvariable=StringVar(),
                         text=Configer.get_para("pH"), x=110, y=second_y + 2, width=30)
        create_tooltip(self.ph.entry, "按照一定的规则在指定pH生成质子化状态。为obabel内置"
                                      "方法，对某些氨基酸可能会发生变化，结果不一定可靠。")

        # 能量最小化
        self.is_minimize = SCheckbutton(choose_output_ligand_labelframe, text="能量最小化",
                                        variable=StringVar(),
                                        value=Configer.get_para("is_minimize"),
                                        x=200, y=second_y)
        create_tooltip(self.is_minimize.checkbutton, "是否对分子进行能量最小化")
        self.is_minimize.checkbutton.bind("<Button-1>", self._disable_minimize)
        SLabel(root=choose_output_ligand_labelframe, text="力场", x=290, y=second_y)
        minimize_value = ("MMFF94", "MMFF94s", "GAFF", "Chemical", "UFF")
        self.minimize = SCombbox(root=choose_output_ligand_labelframe,
                                 textvariable=StringVar(), values=minimize_value,
                                 default_value=Configer.get_para("minimize"),
                                 x=325, y=second_y, width=100)
        create_tooltip(self.minimize.combobox, "能量最小化使用的力场，推荐MMFF94")

        # 默认
        default_button = SButton(root=choose_output_ligand_labelframe, text="默认",
                                 x=450, y=second_y - 2)
        default_button.button.bind("<Button-1>", self._default)
        create_tooltip(default_button.button, "恢复默认值")

        # 初始化状态
        if self.is_minimize.variable.get() == "0" or self.is_minimize.variable.get() == "":
            self.minimize.combobox.configure(state="disable")

        # 第三排
        third_y = 60
        choose_output_dir_button = SButton(choose_output_ligand_labelframe, text="选择输出文件夹",
                                           x=10, y=third_y)
        create_tooltip(choose_output_dir_button.button, "选择配体输出的文件夹")
        self.choose_output_dir_entry = SEntry(root=choose_output_ligand_labelframe,
                                              textvariable=StringVar(),
                                              text=Configer.get_para("ligand_output_dir"),
                                              x=110, y=third_y + 4, width=450)
        create_tooltip(self.choose_output_dir_entry.entry, "所选的输出目录")
        choose_output_dir_button.bind_open_dir(entry_text=self.choose_output_dir_entry.textvariable,
                                               title="选择要输出配体的文件夹")

    def _disable_minimize(self, event):
        state = self.is_minimize.variable.get()
        if state == "1":
            self.minimize.combobox.configure(state="disable")
        elif state == "0" or state == "":
            self.minimize.combobox.configure(state="readonly")

    def _default(self, event):
        self.ph.textvariable.set("7.4")
        self.gen3d.variable.set("1")
        self.is_minimize.variable.set("1")
        self.minimize.textvariable.set("MMFF94")
        self.is_minimize.checkbutton.configure(state="normal")
        self.minimize.combobox.configure(state="readonly")

    def _create_convert(self):
        y = 230
        convert_button = SButton(root=self.root, x=10, y=y, text="开始转换")
        create_tooltip(convert_button.button, "开始转换")
        self.progress = Progressbar(self.root, mode="determinate")
        self.progress.place(x=100, y=y + 2, width=400)
        create_tooltip(self.progress, "转换进度")
        self.progress_label = SLabel(self.root, text="没有任务", x=510, y=y)
        convert_button.button.bind("<Button-1>", self._start_convert)

    def _start_convert(self, event):
        if not Check.check_obabel():
            return

        if not Check.check_python():
            return

        input_files = self.choose_ligands_entry.textvariable.get()

        # 判断输入内容不能包含空格
        if Check.has_space(input_files):
            messagebox.showerror("输入错误！", "输入路径不能包含空格！")
            return

        input_format = self.input_format.textvariable.get()
        input_ligands = []

        # 判断输入的内容
        if input_files.endswith(";"):
            if input_files.split(".")[-1][0:-1] != input_format:
                messagebox.showerror("错误！", "选择的配体和输入的配体不符合！")
                return
            input_ligands.extend(input_files.split(";")[0:-1])
        elif os.path.isdir(input_files):
            list_file = os.listdir(input_files)
            for file in list_file:
                if file.endswith(input_format):
                    input_ligands.append(input_files + os.sep + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含选择格式的配体！")
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        ph = self.ph.textvariable.get()
        # ph不能为空
        if ph == "":
            messagebox.showerror("错误！", "请输入pH！")
            return

        gen3d = self.gen3d.variable.get()
        is_minimize = self.is_minimize.variable.get()
        minimize = self.minimize.textvariable.get()
        output_format = self.output_format.textvariable.get()
        output_path = self.choose_output_dir_entry.textvariable.get()

        # 输出目录不能为空
        if output_path == "" or output_path.count(" ") > 0:
            messagebox.showerror("输入错误！", "输出路径不能包含空格！")
            return
        if not os.path.exists(output_path):
            messagebox.showerror("输入错误！", "输出路径不存在！")
            return

        if input_format == output_format:
            messagebox.showerror("错误！", "输入和输出格式不应相等！")
            return

        output_ligands = []

        for ligand in input_ligands:
            ligand_name = ligand.split(os.sep)[-1].split(".")[0] + "." + output_format
            output_ligands.append(output_path + os.sep + ligand_name)

        self.progress["maximum"] = len(input_ligands)

        # 进行格式转换
        if input_format == "pdbqt":  # pdbqt->other
            # pdbqt->pdb
            if output_format == "pdb":
                i = 0
                while i < len(input_ligands):
                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1
                    self.progress.update()

                    pdbqt_2_pdb(input_ligands[i], output_ligands[i])
                    i += 1
                messagebox.showinfo("转换完成！", "成功将pdbqt转换成pdb！")
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return
            # pdbqt->other
            else:
                # obabel转换成输出格式，先转成pdb
                pdb_ligands = []
                for ligand in input_ligands:
                    ligand_name = ligand.split(os.sep)[-1].split(".")[0] + ".pdb"
                    pdb_ligands.append(output_path + os.sep + "tmp" + os.sep + ligand_name)

                self.progress["maximum"] = len(input_ligands) * 2

                mk_output_dir(output_path + os.sep + "tmp")  # 创建临时文件夹

                i = 0
                while i < len(input_ligands):
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    self.progress["value"] = i + 1
                    self.progress.update()

                    pdbqt_2_pdb(input_ligands[i], pdb_ligands[i])
                    i += 1

                i = 0
                while i < len(input_ligands):
                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1 + len(input_ligands)
                    self.progress.update()

                    pdb_2_other(pdb_ligands[i], output_ligands[i])
                    i += 1

                # 删除临时pdb文件
                shutil.rmtree(output_path + os.sep + "tmp")
                messagebox.showinfo("转换完成！", "成功将pdbqt转换%s！" % output_format)
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return

        # pdb/mol2->pdbqt
        elif (input_format == "pdb" or input_format == "mol2") and output_format == "pdbqt":
            i = 0
            while i < len(input_ligands):
                # 更改标签文字
                label_text = "%i/%i" % (i + 1, len(input_ligands))
                self.progress_label.label.configure(text=label_text)
                self.progress_label.label.update()

                # 更新进度条
                self.progress["value"] = i + 1 + len(input_ligands)
                self.progress.update()

                pdb_mol2_2_pdbqt(input_ligands[i], output_ligands[i])
                i += 1
            messagebox.showinfo("转换完成！", "成功将%s转换pdbqt！" % input_format)
            self.progress["value"] = 0
            self.progress_label.label.configure(text="没有任务")
            return

        else:
            # mol/smi->pdbqt
            if input_format == "mol" or input_format == "smi" and output_format == "pdbqt":
                pdb_ligands = []
                for ligand in input_ligands:
                    ligand_name = ligand.split(os.sep)[-1].split(".")[0] + ".pdb"
                    pdb_ligands.append(output_path + os.sep + "tmp" + os.sep + ligand_name)

                self.progress["maximum"] = len(input_ligands) * 2

                mk_output_dir(output_path + os.sep + "tmp")  # 创建临时文件夹

                i = 0
                while i < len(input_ligands):
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    self.progress["value"] = i + 1
                    self.progress.update()

                    two_d_2_pdb(input_ligands[i], pdb_ligands[i], ph, minimize)
                    i += 1

                i = 0
                while i < len(input_ligands):
                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1 + len(input_ligands)
                    self.progress.update()

                    pdb_mol2_2_pdbqt(pdb_ligands[i], output_ligands[i])
                    i += 1
                # 删除临时pdb文件
                shutil.rmtree(output_path + os.sep + "tmp")
                messagebox.showinfo("转换完成！", "成功将%s转换pdbqt！" % input_format)
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return
            # sdf->pdbqt
            elif (input_format == "sdf" or input_format == "xyz") and output_format == "pdbqt":
                # 先转pdb
                pdb_ligands = []
                for ligand in input_ligands:
                    ligand_name = ligand.split(os.sep)[-1].split(".")[0] + ".pdb"
                    pdb_ligands.append(output_path + os.sep + "tmp" + os.sep + ligand_name)

                self.progress["maximum"] = len(input_ligands) * 2

                mk_output_dir(output_path + os.sep + "tmp")  # 创建临时文件夹

                i = 0
                while i < len(input_ligands):
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    self.progress["value"] = i + 1
                    self.progress.update()

                    three_d_2_pdb(input_ligands[i], pdb_ligands[i], is_minimize, minimize)
                    i += 1

                i = 0
                while i < len(input_ligands):
                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1 + len(input_ligands)
                    self.progress.update()

                    pdb_mol2_2_pdbqt(pdb_ligands[i], output_ligands[i])
                    i += 1
                # 删除临时pdb文件
                shutil.rmtree(output_path + os.sep + "tmp")
                messagebox.showinfo("转换完成！", "成功将%s转换pdbqt！" % input_format)
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return
            # mol/smi/sdf/mol2/pdb/xyz->pdb/sdf/mol2/xyz
            else:
                if gen3d == "1":
                    # 3D并最小化
                    if is_minimize == "1":
                        i = 0
                        while i < len(input_ligands):
                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            ob_3d_min(input_ligands[i], output_ligands[i], ph, minimize)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")
                    # 3D不最小化
                    else:
                        i = 0
                        while i < len(input_ligands):
                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            ob_3d(input_ligands[i], output_ligands[i], ph)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")
                else:
                    # 不3D并最小化
                    if is_minimize == "1":
                        i = 0
                        while i < len(input_ligands):
                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            ob_min(input_ligands[i], output_ligands[i], ph, minimize)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")
                    # 不3D也不最小化
                    else:
                        i = 0
                        while i < len(input_ligands):
                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            ob(input_ligands[i], output_ligands[i])
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")

    def save_para(self):
        self.config.para_dict["input_format"] = self.input_format.textvariable.get()
        self.config.para_dict["choose_ligands"] = self.choose_ligands_entry.textvariable.get()
        self.config.para_dict["output_format"] = self.output_format.textvariable.get()
        self.config.para_dict["gen3d"] = self.gen3d.variable.get()
        self.config.para_dict["pH"] = self.ph.textvariable.get()
        self.config.para_dict["is_minimize"] = self.is_minimize.variable.get()
        self.config.para_dict["minimize"] = self.minimize.textvariable.get()
        self.config.para_dict["ligand_output_dir"] = self.choose_output_dir_entry.textvariable.get()


if __name__ == '__main__':
    print(os.sep)
