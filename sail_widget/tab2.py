from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from sail_widget.s_button import HelpButton
from sail_widget.tooltip import create_tooltip
from sail_widget.s_label import SLabel
from sail_widget.s_entry import SEntry
from sail_widget.s_button import SButton

from tools.configer import Configer, ConfigReader, ConfigWriter
from tools.text import *
from tools.number import *
from tools.genbox import Box


class Tab2(object):  # 配置config.txt

    def __init__(self, tab: Frame, config: Configer):
        """
        创建一个选项卡,需要父窗口和用来保存配置的配置器
        :param tab: 选项卡
        :param config:  配置器
        """
        # 变量
        self.root = tab
        self.config = config

        # 创建分块内容
        self._create_main_frame()
        self._create_option_frame()
        self._create_tools_frame()
        self._create_output_frame()

        # 帮助按钮
        self.help_button = HelpButton(root=self.root, help_text=TAB2_HELP_TEXT,
                                      x=410, y=300, width=BUTTON_WIDTH)
        create_tooltip(self.help_button.help_button, "获取帮助")

    def _create_main_frame(self):
        self.main_label_frame = LabelFrame(self.root, text="主要参数")
        self.main_label_frame.place(x=10, y=10, width=320, height=120)

        # center_x
        SLabel(self.main_label_frame, text="center_x = ",
               x=10, y=5)
        self.center_x = SEntry(self.main_label_frame, textvariable=StringVar(),
                               text=Configer.get_para("center_x"),
                               x=95, y=5, width=60)
        create_tooltip(self.center_x.entry, "对接位点的x坐标")

        # center_y
        SLabel(self.main_label_frame, text="center_y = ",
               x=10, y=35)
        self.center_y = SEntry(self.main_label_frame, textvariable=StringVar(),
                               text=Configer.get_para("center_y"),
                               x=95, y=35, width=60)
        create_tooltip(self.center_y.entry, "对接位点的y坐标")

        # center_z
        SLabel(self.main_label_frame, text="center_z = ", x=10, y=65)
        self.center_z = SEntry(self.main_label_frame, textvariable=StringVar(),
                               text=Configer.get_para("center_z"),
                               x=95, y=65, width=60)
        create_tooltip(self.center_z.entry, "对接位点的z坐标")

        # size_x
        SLabel(self.main_label_frame, text="size_x = ",
               x=175, y=5)
        self.size_x = SEntry(self.main_label_frame, textvariable=StringVar(),
                             text=Configer.get_para("size_x"),
                             x=245, y=5, width=60)
        create_tooltip(self.size_x.entry, "对接位点的x方向大小")

        # size_y
        SLabel(self.main_label_frame, text="size_y = ",
               x=175, y=35)
        self.size_y = SEntry(self.main_label_frame, textvariable=StringVar(),
                             text=Configer.get_para("size_y"),
                             x=245, y=35, width=60)
        create_tooltip(self.size_y.entry, "对接位点的y方向大小")

        # size_z
        SLabel(self.main_label_frame, text="size_z = ",
               x=175, y=65)
        self.size_z = SEntry(self.main_label_frame, textvariable=StringVar(),
                             text=Configer.get_para("size_z"),
                             x=245, y=65, width=60)
        create_tooltip(self.size_z.entry, "对接位点的z方向大小")

    def _create_option_frame(self):
        self.option_label_frame = LabelFrame(self.root, text="可选")
        self.option_label_frame.place(x=340, y=10, width=240, height=120)

        # exhaustiveness
        SLabel(self.option_label_frame, text="exhaustiveness = ",
               x=10, y=5)
        self.exhaustiveness = SEntry(self.option_label_frame, textvariable=StringVar(),
                                     text=Configer.get_para("exhaustiveness"),
                                     x=140, y=5, width=20)
        create_tooltip(self.exhaustiveness.entry, "搜索度，越大耗时越长，建议保持默认")

        # num_modes
        SLabel(self.option_label_frame, text="num_modes = ",
               x=10, y=35)
        self.num_modes = SEntry(self.option_label_frame, textvariable=StringVar(),
                                text=Configer.get_para("num_modes"),
                                x=140, y=35, width=20)
        create_tooltip(self.num_modes.entry, "最多生成多少种结合模式")

        # energy_range
        SLabel(self.option_label_frame, text="energy_range = ",
               x=10, y=65)
        self.energy_range = SEntry(self.option_label_frame, textvariable=StringVar(),
                                   text=Configer.get_para("energy_range"),
                                   x=140, y=65, width=20)

        create_tooltip(self.energy_range.entry, "最大最小结合模式能量差")

        # 恢复默认值
        default_button = SButton(self.option_label_frame, text="默认", x=170, y=62, width=60)
        default_button.button.bind("<Button-1>", self._change_default)
        create_tooltip(default_button.button, "恢复默认值")

    def _change_default(self, event):
        self.exhaustiveness.textvariable.set(8)
        self.num_modes.textvariable.set(9)
        self.energy_range.textvariable.set(3)

    def _create_tools_frame(self):
        self.tools_frame = LabelFrame(self.root, text="工具")
        self.tools_frame.place(x=10, y=140, width=570, height=100)

        # 读取配置文件
        self.read_config_button = SButton(self.tools_frame, "读取配置文件", 10, 10)
        create_tooltip(self.read_config_button.button, "必须选择config.txt文件！")
        self.read_config_entry = SEntry(root=self.tools_frame, textvariable=StringVar(),
                                        text=Configer.get_para("read_config"),
                                        x=100, y=14, width=360)
        create_tooltip(self.read_config_entry.entry, "你选择的config.txt文件位置")
        self.read_config_button.bind_open_file(entry_text=self.read_config_entry.textvariable,
                                               title="请选择config.txt文件",
                                               file_type="txt")
        self.read_button = SButton(self.tools_frame, "读取到参数", 470, 10)
        create_tooltip(self.read_button.button, "读取到上方")
        self.read_button.button.bind("<Button-1>", self.read_config)

        # 自动生成盒子
        self.choose_raw_ligand_button = SButton(self.tools_frame, "读取共晶配体", 10, 40)
        create_tooltip(self.choose_raw_ligand_button.button, "必须选择共晶配体pdbqt文件！")
        self.choose_raw_ligand_entry = SEntry(root=self.tools_frame, textvariable=StringVar(),
                                              text=Configer.get_para("choose_raw_ligand"),
                                              x=100, y=44, width=360)
        self.choose_raw_ligand_button.bind_open_file(entry_text=self.choose_raw_ligand_entry.textvariable,
                                                     title="请选择“共晶配体”PDBQT文件！",
                                                     file_type="pdbqt")
        create_tooltip(self.choose_raw_ligand_entry.entry, "你选择的共晶配体pdbqt文件位置")
        self.gen_box_button = SButton(self.tools_frame, "计算对接位点", 470, 40)
        create_tooltip(self.gen_box_button.button, "自动计算对接位点，该对接位点为共晶配体的"
                                                   "最小外切正方体，结果仅供参考。")
        self.gen_box_button.button.bind("<Button-1>", self.gen_box)

    def _create_output_frame(self):
        self.output_frame = LabelFrame(self.root, text="输出配置文件")
        self.output_frame.place(x=10, y=250, width=570, height=50)

        # 输出配置文件
        self.output_config_button = SButton(self.output_frame, "选择输出目录", 10, 0)
        create_tooltip(self.output_config_button.button, "选择config.txt输出的目录")
        self.output_config_entry = SEntry(root=self.output_frame, textvariable=StringVar(),
                                          text=Configer.get_para("output_config"),
                                          x=100, y=4, width=360)
        create_tooltip(self.output_config_entry.entry, "输出config.txt文件的位置")
        self.output_config_button.bind_open_dir(self.output_config_entry.textvariable, title="选择输出目录")
        self.gen_config_button = SButton(self.output_frame, "输出", 470, 0)
        create_tooltip(self.gen_config_button.button, "开始输出")
        self.gen_config_button.button.bind("<Button-1>", self.output_config)

    def read_config(self, event):
        # 判断是否是config.txt
        if not self.read_config_entry.textvariable.get().endswith("config.txt"):
            messagebox.showerror(title="错误", message="请选择config.txt文件！")
            return

        with open(self.read_config_entry.textvariable.get(), "r") as f:
            for line in f.readlines():
                para_name, para = ConfigReader.get_config_para(line)
                if para_name == "center_x":
                    self.center_x.textvariable.set(para)
                elif para_name == "center_y":
                    self.center_y.textvariable.set(para)
                elif para_name == "center_z":
                    self.center_z.textvariable.set(para)
                elif para_name == "size_x":
                    self.size_x.textvariable.set(para)
                elif para_name == "size_y":
                    self.size_y.textvariable.set(para)
                elif para_name == "size_z":
                    self.size_z.textvariable.set(para)
                elif para_name == "exhaustiveness":
                    self.exhaustiveness.textvariable.set(para)
                elif para_name == "num_modes":
                    self.num_modes.textvariable.set(para)
                elif para_name == "energy_range":
                    self.energy_range.textvariable.set(para)
                elif para_name == "":
                    continue
                else:
                    messagebox.showwarning("未知参数！", "包含未知参数\"%s\"" % para_name)
                    continue

    def output_config(self, event):

        # 判断盒子大小
        size_x = float(self.size_x.textvariable.get())
        size_y = float(self.size_y.textvariable.get())
        size_z = float(self.size_z.textvariable.get())

        box_size = size_x * size_y * size_z
        if box_size >= 27000:
            messagebox.showerror("错误！", "盒子总大小应小于27000，当前%.2f，请减小盒子大小！" % box_size)
            return

        if self.output_config_entry.textvariable.get() == "":
            messagebox.showerror("错误！", "请选择输出路径！")
            return

        config_dict = {"center_x = ": self.center_x.textvariable.get(),
                       "center_y = ": self.center_y.textvariable.get(),
                       "center_z = ": self.center_z.textvariable.get(),
                       "size_x = ": size_x,
                       "size_y = ": size_y,
                       "size_z = ": size_z,
                       "exhaustiveness = ": self.exhaustiveness.textvariable.get(),
                       "num_modes = ": self.num_modes.textvariable.get(),
                       "energy_range = ": self.energy_range.textvariable.get()
                       }
        output_path = self.output_config_entry.textvariable.get()
        ConfigWriter.write_config(config_dict, output_path)
        messagebox.showinfo("导出配置文件成功！", "配置文件已经导出到：\n%s/config.txt" % output_path)

    def gen_box(self, event):
        if not self.choose_raw_ligand_entry.textvariable.get().endswith(".pdbqt"):
            messagebox.showerror("错误！", "请选择pdbqt文件！")
            return

        box = Box(self.choose_raw_ligand_entry.textvariable.get())
        try:
            center_x, center_y, center_z, box_size = box.get_box()
        except ZeroDivisionError:
            messagebox.showerror("错误！", "请确保选择的是共晶的pdbqt配体！")
        else:
            self.center_x.textvariable.set(center_x)
            self.center_y.textvariable.set(center_y)
            self.center_z.textvariable.set(center_z)
            self.size_x.textvariable.set(box_size)
            self.size_y.textvariable.set(box_size)
            self.size_z.textvariable.set(box_size)
            messagebox.showinfo("成功！", "已自动计算位点，仅供参考！")

    def save_para(self):
        self.config.para_dict["center_x"] = self.center_x.textvariable.get()
        self.config.para_dict["center_y"] = self.center_y.textvariable.get()
        self.config.para_dict["center_z"] = self.center_z.textvariable.get()
        self.config.para_dict["size_x"] = self.size_x.textvariable.get()
        self.config.para_dict["size_y"] = self.size_y.textvariable.get()
        self.config.para_dict["size_z"] = self.size_z.textvariable.get()

        self.config.para_dict["exhaustiveness"] = self.exhaustiveness.textvariable.get()
        self.config.para_dict["num_modes"] = self.num_modes.textvariable.get()
        self.config.para_dict["energy_range"] = self.energy_range.textvariable.get()

        self.config.para_dict["read_config"] = self.read_config_entry.textvariable.get()
        self.config.para_dict["choose_raw_ligand"] = self.choose_raw_ligand_entry.textvariable.get()
        self.config.para_dict["output_config"] = self.output_config_entry.textvariable.get()
