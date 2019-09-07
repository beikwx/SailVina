from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from sail_widget.s_button import HelpButton
from sail_widget.tooltip import create_tooltip
from sail_widget.s_label import SLabel
from sail_widget.s_entry import SEntry
from sail_widget.s_button import SButton

from tools.check import Check
from tools.text import *
from tools.configer import Configer
from tools.file_path import *
from tools.file_processor import get_config_files
from tools.dock_processor import vina_dock


# 分子对接
class Tab4(object):

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        # 需要保存的参数
        self.choose_ligand_entry = None
        self.choose_proteins_entry = None
        self.choose_output_entry = None
        self.times_entry = None

        # 不需要保存的参数
        self.docking_time_label = None

        self._choose_ligand_frame()
        self._choose_protein_frame()
        self._choose_output_frame()
        self._choose_docking_config()

        self._start_docking()

        # 帮助按钮
        help_button = HelpButton(root=self.root, help_text=TAB4_HELP_TEXT, x=410, y=300, width=80)
        create_tooltip(help_button.help_button, "获取帮助")

    def _choose_ligand_frame(self):
        choose_ligand_labelframe = LabelFrame(self.root, text="选择配体")
        choose_ligand_labelframe.place(x=10, y=10, width=570, height=50)

        choose_ligands = SButton(root=choose_ligand_labelframe, text="选择单/多个配体", x=10, y=0)
        create_tooltip(choose_ligands.button, "选择单/多个配体，配体格式必须是pdbqt！")
        choose_ligand_dir = SButton(root=choose_ligand_labelframe, text="选择文件夹", x=110, y=0)
        create_tooltip(choose_ligand_dir.button, "选择包含pdbqt格式配体的文件夹。")
        self.choose_ligand_entry = SEntry(root=choose_ligand_labelframe, textvariable=StringVar(),
                                          text=Configer.get_para("choose_docking_ligands"),
                                          x=200, y=4, width=360)
        create_tooltip(self.choose_ligand_entry.entry, "选择的配体或者包含配体的文件夹")
        choose_ligands.bind_open_files(entry_text=self.choose_ligand_entry.textvariable,
                                       title="选择单/多个配体",
                                       file_type="pdbqt")
        choose_ligand_dir.bind_open_dir(entry_text=self.choose_ligand_entry.textvariable,
                                        title="选择包含pdbqt配体的文件夹")

    def _choose_protein_frame(self):
        choose_protein_labelframe = LabelFrame(self.root, text="选择受体")
        choose_protein_labelframe.place(x=10, y=70, width=570, height=50)

        choose_proteins = SButton(root=choose_protein_labelframe, text="选择受体文件夹", x=10, y=0)
        create_tooltip(choose_proteins.button, "选择受体文件夹。受体必须命名为preped.pdbqt\n"
                                               "单个受体请选择包含这个受体的文件夹\n"
                                               "多个受体请选择包含多个受体文件夹的文件夹\n"
                                               "详情见帮助及教程")
        self.choose_proteins_entry = SEntry(root=choose_protein_labelframe, textvariable=StringVar(),
                                            text=Configer.get_para("choose_docking_proteins"),
                                            x=110, y=4, width=450)
        create_tooltip(self.choose_proteins_entry.entry, "包含受体的文件夹")
        choose_proteins.bind_open_dir(entry_text=self.choose_proteins_entry.textvariable,
                                      title="选择包含pdbqt受体的文件夹")

    def _choose_output_frame(self):
        choose_output_labelframe = LabelFrame(self.root, text="结果输出")
        choose_output_labelframe.place(x=10, y=130, width=570, height=50)

        choose_output = SButton(root=choose_output_labelframe, text="选择输出文件夹", x=10, y=0)
        create_tooltip(choose_output.button, "选择对接结果输出目录")
        self.choose_output_entry = SEntry(root=choose_output_labelframe, textvariable=StringVar(),
                                          text=Configer.get_para("choose_docking_output"),
                                          x=110, y=4, width=450)
        create_tooltip(self.choose_output_entry.entry, "所选的对接结果输出目录")
        choose_output.bind_open_dir(entry_text=self.choose_output_entry.textvariable,
                                    title="选择对接输出的文件夹")

    def _choose_docking_config(self):
        choose_config_labelframe = LabelFrame(self.root, text="对接配置")
        choose_config_labelframe.place(x=10, y=190, width=570, height=50)

        self.docking_time_label = SLabel(root=choose_config_labelframe, text="对接次数：", x=10, y=0)

        self.times_entry = SEntry(root=choose_config_labelframe,
                                  textvariable=StringVar(),
                                  text=Configer.get_para("docking_times"),
                                  x=80, y=0, width=20)
        create_tooltip(self.times_entry.entry, "每个配体需要对接的次数")

    def _start_docking(self):
        y = 250
        docking_button = SButton(root=self.root, text="开始对接", x=10, y=y)
        create_tooltip(docking_button.button, "使用Vina进行对接")

        self.progress = Progressbar(self.root, mode="determinate")
        self.progress.place(x=100, y=y + 2, width=400)
        create_tooltip(self.progress, "对接进度")

        self.progress_label = SLabel(self.root, text="没有任务", x=510, y=y)
        docking_button.button.bind("<Button-1>", self._docking)

        text_y = 276
        current_protein_frame = Frame(self.root, width=200, height=40)
        current_protein_frame.place(x=10, y=text_y)
        self.current_protein = SLabel(root=current_protein_frame, text="", x=0, y=0)
        current_ligand_frame = Frame(self.root, width=200, height=50)
        current_ligand_frame.place(x=220, y=text_y)
        self.current_ligand = SLabel(root=current_ligand_frame, text="", x=0, y=0)
        current_time_frame = Frame(self.root, width=150, height=50)
        current_time_frame.place(x=430, y=text_y)
        self.current_time = SLabel(root=current_time_frame, text="", x=0, y=0)

    def _docking(self, event):
        input_ligands_full = self.choose_ligand_entry.entry.get()
        receptor_dir = self.choose_proteins_entry.entry.get()
        output_dir = self.choose_output_entry.entry.get()
        docking_times = self.times_entry.entry.get()

        # 所有选择的路径和文件都不能为空和包含空格。
        if (Check.check_path(input_ligands_full) or Check.check_path(receptor_dir)
                or Check.check_path(output_dir) or Check.check_path(docking_times)):
            messagebox.showerror("输入错误", "所有参数不能为空或者包含空格")
            return

        try:
            times = int(docking_times)
        except ValueError:
            messagebox.showerror("错误！", "对接次数必须是数字！")
            return

        # 如果不存在输出文件夹就创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        input_ligands = []

        # 输入的配体
        if input_ligands_full.endswith(";"):  # 如果是单个或者多个配体
            # 必须是pdbqt文件
            if input_ligands_full.split(".")[-1][0:-1] != "pdbqt":
                messagebox.showerror("错误！", "配体必须是pdbqt格式！")
                return
            input_ligands.extend(input_ligands_full.split(";")[0:-1])
        elif os.path.isdir(input_ligands_full):
            # 如果选择的是目录
            list_file = os.listdir(input_ligands_full)
            for file in list_file:
                if file.endswith("pdbqt"):
                    input_ligands.append(input_ligands_full + os.sep + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含pdbqt格式的配体！")
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        # 输入的受体
        receptors = []
        # 选择了一个受体
        if os.path.exists("%s" % receptor_dir + os.sep + "preped.pdbqt"):
            if not Check.check_config(receptor_dir):
                messagebox.showerror("错误！", "受体中没有config.txt文件！")
                return
            receptors.append("%s" % receptor_dir + os.sep + "preped.pdbqt")
        # 可能选择了多个受体
        else:
            if not os.path.exists(receptor_dir):
                messagebox.showerror("错误！", "所选受体目录不存在！")
                return
            child_receptor = os.listdir(receptor_dir)
            for receptor in child_receptor:
                if os.path.exists("%s" % receptor_dir + os.sep + "%s" % receptor + os.sep + "preped.pdbqt"):
                    if not Check.check_config("%s" % receptor_dir + os.sep + "%s" % receptor):
                        messagebox.showwarning("警告！", "受体%s中没有config.txt文件，将不进行对接！" % receptor)
                        continue
                    receptors.append("%s" % receptor_dir + os.sep + "%s" % receptor + os.sep + "preped.pdbqt")
        if len(receptors) == 0:
            messagebox.showerror("错误！", "没有受体，请检查选择的文件夹或者子文件夹中是否"
                                        "包含preped.pdbqt文件!")
            return

        self.progress["maximum"] = len(receptors) * len(input_ligands)
        for receptor in receptors:
            # 在输出目录创建受体的文件夹
            output_dir_r = "%s" % output_dir + os.sep + "%s" % receptor.split(os.sep)[-2]
            # 读取受体中的config文件
            config_files = get_config_files(os.path.split(receptor)[0])
            if not os.path.exists(output_dir_r):
                os.mkdir(output_dir_r)

            for ligand in input_ligands:
                # 初始化循环次数
                i = 0

                # 更新进度条和标签
                current_num = receptors.index(receptor) * len(input_ligands) + input_ligands.index(ligand) + 1
                max_num = len(receptors) * len(input_ligands)
                label_text = "%s/%s" % (current_num, max_num)

                self.progress_label.label.configure(text=label_text)
                self.progress_label.label.update()

                self.progress["value"] = current_num
                self.progress.update()

                current_protein = "当前受体：%s" % receptor.split(os.sep)[-2]
                self.current_protein.label.configure(text=current_protein)
                self.current_protein.label.update()

                current_ligand = "当前配体：%s" % ligand.split(os.sep)[-1].split(".")[0]
                self.current_ligand.label.configure(text=current_ligand)
                self.current_ligand.label.update()

                current_time = "当前次数：%i" % (i + 1)
                self.current_time.label.configure(text=current_time)
                self.current_time.label.update()

                # 开始对接
                while i < times:
                    dock_time = i + 1
                    for config in config_files:
                        ligand_basename = ligand.split(os.sep)[-1].split(".")[0]
                        config_name = os.path.splitext(config)[0].split(os.sep)[-1]
                        output = "%s" % output_dir_r + os.sep +\
                                 "%s_%s_out%s.pdbqt" % (ligand_basename, config_name, dock_time)
                        print(output)
                        vina_dock(ligand, receptor, config, output)
                    i += 1
        messagebox.showinfo("成功！", "对接完成！")
        self.progress_label.label.configure(text="没有任务")
        self.progress_label.label.update()

        self.progress["value"] = 0
        self.progress.update()

        self.current_protein.label.configure(text="")
        self.current_protein.label.update()

        self.current_ligand.label.configure(text="")
        self.current_ligand.label.update()

        self.current_time.label.configure(text="")
        self.current_time.label.update()

    def save_para(self):
        self.config.para_dict["choose_docking_ligands"] = self.choose_ligand_entry.textvariable.get()
        self.config.para_dict["choose_docking_proteins"] = self.choose_proteins_entry.textvariable.get()
        self.config.para_dict["choose_docking_output"] = self.choose_output_entry.textvariable.get()
        self.config.para_dict["docking_times"] = self.times_entry.textvariable.get()
