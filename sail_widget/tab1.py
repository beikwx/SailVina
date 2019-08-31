import webbrowser
from contextlib import closing

import requests

from tkinter import *
from tkinter.ttk import *

from sail_widget.tooltip import create_tooltip
from sail_widget.s_button import SButton
from sail_widget.s_button import HelpButton
from sail_widget.s_label import SLabel
from sail_widget.s_entry import SEntry
from sail_widget.s_toplevel import STopLevel
from sail_widget.s_checkbox import SCheckbutton
from sail_widget.s_combobox import SCombbox

from tools.text import *
from tools.number import *
from tools.check import *
from tools.receptor_processor import *
from tools.file_path import *
from tools.format_convertor import pdb_mol2_2_pdbqt


# 准备受体
class Tab1(object):
    chains = None

    def __init__(self, tab, configer):
        self.root = tab
        self.configer = configer

        # 需要保存的参数
        self.pdb_id_entry = None
        self.pdb_save_path_entry = None
        self.ligand_save_path_entry = None
        self.choose_prepare_output_path = None
        self.output_path = None
        self.is_fix_receptor = None
        self.preserve_charges = None
        self.nphs = None
        self.lps = None
        self.waters = None
        self.nonstdres = None

        # 不需要保存的参数
        self.download_progressbar = None
        self.download_state_label = None
        self.choose_raw_receptor_entry = None

        # 受体信息
        self.model_list = None
        self.model_name = None
        self.chain_list = None
        self.chain_name = None
        self.ligand_list = None
        self.ligand_name = None
        self.fix_method = None

        # 下载受体
        self.create_download_receptor()

        # 准备受体
        self.create_prepared_receptor()

        # 帮助按钮
        self.help_button = HelpButton(root=self.root, help_text=TAB1_HELP_TEXT,
                                      x=HELP_BUTTON_X, y=HELP_BUTTON_Y, width=BUTTON_WIDTH)

    def create_prepared_receptor(self):
        # 总框架
        prepared_receptor_labelframe = LabelFrame(self.root, text="准备受体")
        prepared_receptor_labelframe.place(x=LEFT_X, y=130, width=FULL_NOTEBOOK_WIDTH, height=170)

        # 第一排,选择受体
        choose_raw_receptor_button = SButton(prepared_receptor_labelframe,
                                             text="选择单个受体", x=LEFT_X, y=0)
        create_tooltip(choose_raw_receptor_button.button, "选择要进行准备的单个pdb受体")

        choose_raw_receptors_button = SButton(prepared_receptor_labelframe,
                                              text="选择多个受体", x=LEFT_X + 90, y=0)
        create_tooltip(choose_raw_receptors_button.button, "选择要进行准备的包含多个pdb受体的文件夹")

        self.choose_raw_receptor_entry = SEntry(prepared_receptor_labelframe,
                                                textvariable=StringVar(),
                                                text=Configer.get_para("raw_receptor_path"),
                                                x=190, y=3, width=270)
        create_tooltip(self.choose_raw_receptor_entry.entry, "选择的受体")

        # 绑定打开事件
        choose_raw_receptor_button.bind_open_file(entry_text=self.choose_raw_receptor_entry.textvariable,
                                                  title="选择受体pdb文件", file_type="pdb")
        choose_raw_receptors_button.bind_open_dir(entry_text=self.choose_raw_receptor_entry.textvariable,
                                                  title="选择包含pdb受体文件的文件夹")

        get_info_button = SButton(prepared_receptor_labelframe, text="受体信息",
                                  x=470, y=0)
        get_info_button.button.bind("<Button-1>", self.getinfo)
        create_tooltip(get_info_button.button, "查看受体信息")

        # 第二排，提取配体保存的路径
        ligand_save_path_button = SButton(prepared_receptor_labelframe,
                                          text="配体输出路径", x=10, y=30)
        create_tooltip(ligand_save_path_button.button, "选择提取的配体要保存的位置")
        self.ligand_save_path_entry = SEntry(prepared_receptor_labelframe,
                                             textvariable=StringVar(),
                                             text=Configer.get_para("extract_ligand_path"),
                                             x=100, y=33, width=360)
        create_tooltip(self.ligand_save_path_entry.entry, "提取的配体保存的目录，不存在将创建文件夹")
        ligand_save_path_button.bind_open_dir(entry_text=self.ligand_save_path_entry.textvariable,
                                              title="选择要保存的路径")

        save_ligand_button = SButton(prepared_receptor_labelframe, text="提取配体",
                                     x=470, y=30)
        save_ligand_button.button.bind("<Button-1>", self.extract_ligand)
        create_tooltip(save_ligand_button.button, "提取受体中的配体")

        # 第三排，准备受体
        save_prepared_receptor_button = SButton(prepared_receptor_labelframe,
                                                text="受体输出路径", x=LEFT_X, y=60)
        create_tooltip(save_prepared_receptor_button.button, "选择准备后的受体保存路径")
        self.choose_prepare_output_path = SEntry(prepared_receptor_labelframe,
                                                 textvariable=StringVar(),
                                                 text=Configer.get_para("preped_path"),
                                                 x=100, y=63, width=360)
        create_tooltip(self.choose_prepare_output_path.entry, "准备受体后的输出目录")
        save_prepared_receptor_button.bind_open_dir(self.choose_prepare_output_path.textvariable,
                                                    title="选择输出目录")

        prepare_receptor_button = SButton(prepared_receptor_labelframe, text="准备受体",
                                          x=470, y=60)
        prepare_receptor_button.button.bind("<Button-1>", self.prepared_receptor)
        create_tooltip(prepare_receptor_button.button, "开始准备受体")

        # 第四排，准备选项
        fourth_y = 90
        SLabel(prepared_receptor_labelframe, text="ADT参数", x=LEFT_X, y=fourth_y)
        SLabel(prepared_receptor_labelframe, text="修复", x=100, y=fourth_y)
        fix_text = ("bonds_hydrogens", "bonds", "hydrogens", "checkhydrogens", "None")
        self.fix_method = SCombbox(root=prepared_receptor_labelframe, textvariable=StringVar(),
                                   values=fix_text,
                                   default_value=Configer.get_para("fix_method"),
                                   x=135, y=fourth_y, width=140)
        create_tooltip(self.fix_method.combobox, "使用ADT方法修复受体\n"
                                                 "bonds_hydrogens：修复键级和加氢\n"
                                                 "bonds：修复键级\n"
                                                 "hydrogens:加氢\n"
                                                 "checkhydrogens：没有氢的地方加氢\n"
                                                 "None:不进行修复")
        self.preserve_charges = SCheckbutton(prepared_receptor_labelframe, text="保留电荷", variable=StringVar(),
                                             value=Configer.get_para("preserve_charges"),
                                             x=290, y=fourth_y)
        create_tooltip(self.preserve_charges.checkbutton, "勾选则保留输入电荷，不勾选添加gasteiger电荷")
        SLabel(prepared_receptor_labelframe, text="|", x=380, y=fourth_y - 2)
        self.is_fix_receptor = SCheckbutton(prepared_receptor_labelframe, text="Biopython功能",
                                            variable=StringVar(),
                                            value=Configer.get_para("fix_receptor"),
                                            x=400, y=fourth_y)
        create_tooltip(self.is_fix_receptor.checkbutton, "只针对单个受体。可以用来检测同源链，提取特定链，"
                                                         "修复受体(受体受损较大可以尝试使用该功能)。"
                                                         "具体修复方法参见biopython官方文档")

        # 第五排，清理格式
        fifth_y = 120
        SLabel(prepared_receptor_labelframe, text="受体处理", x=LEFT_X, y=fifth_y)
        self.nphs = SCheckbutton(prepared_receptor_labelframe, text="nphs",
                                 variable=StringVar(),
                                 value=Configer.get_para("nphs"),
                                 x=LEFT_X + 90, y=fifth_y)
        create_tooltip(self.nphs.checkbutton, "合并非极性氢")
        self.lps = SCheckbutton(prepared_receptor_labelframe, text="lps",
                                variable=StringVar(),
                                value=Configer.get_para("lps"),
                                x=LEFT_X + 150, y=fifth_y)
        create_tooltip(self.lps.checkbutton, "合并电荷，去除孤对电子")
        self.waters = self.waters = SCheckbutton(prepared_receptor_labelframe, text="waters",
                                                 variable=StringVar(),
                                                 value=Configer.get_para("waters"),
                                                 x=LEFT_X + 200, y=fifth_y)
        create_tooltip(self.waters.checkbutton, "去除水")
        self.nonstdres = self.nonstdres = SCheckbutton(prepared_receptor_labelframe, text="nonstdres",
                                                       variable=StringVar(),
                                                       value=Configer.get_para("nonstdres"),
                                                       x=LEFT_X + 270, y=fifth_y)
        create_tooltip(self.nonstdres.checkbutton, "去除非标准氨基酸链(核酸等)")

    def prepared_receptor(self, event):
        input_file = self.choose_raw_receptor_entry.textvariable.get()
        output_path = self.choose_prepare_output_path.textvariable.get()

        fix_receptor = int(self.is_fix_receptor.variable.get())
        fix_method = self.fix_method.textvariable.get()
        preserve_charges = int(self.preserve_charges.variable.get())
        nphs = int(self.nphs.variable.get())
        lps = int(self.lps.variable.get())
        waters = int(self.waters.variable.get())
        nonstdres = int(self.nonstdres.variable.get())

        if not Check.check_python(Configer.get_para("python_path")):
            return

        if Check.check_path(input_file) or Check.check_path(output_path):
            messagebox.showinfo("错误！", "输入输出文件不能包含空格")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("错误", "所选文件或者文件夹不存在!")
            return

        if os.path.isdir(input_file):
            # 选择的是文件夹,批量准备受体
            receptors = get_receptors(input_file)
            input_dir = input_file
            for receptor in receptors:
                input_file = input_dir + os.sep + receptor
                output_file = output_path + os.sep + receptor + "qt"
                prepare_receptor(input_file, output_file, fix_method, preserve_charges, nphs, lps, waters, nonstdres)
            messagebox.showinfo("成功", "成功准备受体！\n注意：自动准备会删除DNA等非标准残基，结果仅供参考。")
            return
        elif input_file.endswith(".pdb"):
            # 如果勾选biopython功能
            if fix_receptor:
                message = ChainExtractor.judge_homo(input_file)
                # 包含同源链。选择同源链，保存到chains列表中。
                if message:
                    warning = ""
                    for content in message:
                        warning += content + "\n"
                    if messagebox.askyesno("检测到同源链", "是否保留只保留特定链？（可多选）\n" + warning):
                        structure = ReceptorProcessor.get_structure(input_file)
                        chains_ids = ReceptorProcessor.get_chain_ids(structure[0])

                        top = STopLevel(self.root, 275, 205, "选择要保存的链").toplevel

                        chains_list = Listbox(top, width=30, height=10, selectmode=EXTENDED)
                        chains_list.place(x=10, y=10, width=255, height=150)
                        self.refresh_listbox(chains_ids, chains_list)
                        scroll = Scrollbar(chains_list)
                        scroll.pack(side=RIGHT, fill=Y)
                        chains_list.configure(yscrollcommand=scroll.set)
                        scroll.config(command=chains_list.yview)

                        def extract_chains():
                            Tab1.chains = []
                            selections = chains_list.curselection()
                            for select in selections:
                                Tab1.chains.append(chains_list.get(select))
                            top.destroy()

                        save_button = SButton(top, "提取链", 10, 170)
                        save_button.button.configure(command=extract_chains)

                        def cancel():
                            Tab1.chains = None
                            top.destroy()

                        cancel_button = SButton(top, "取消", 165, 170)
                        cancel_button.button.configure(command=cancel)

                        top.protocol("WM_DELETE_WINDOW", cancel)

                        self.root.wait_window(top)
                    else:
                        Tab1.chains = []
                else:
                    messagebox.showinfo("没有检测到同源链", "尝试使用biopython进行修复……")
                    Tab1.chains = []

                if Tab1.chains is None:
                    return

                structure = ReceptorProcessor.get_structure(input_file)
                output_file = output_path + os.sep + "bio_fix_" + os.path.split(input_file)[-1]
                ChainExtractor.extract_chain(structure, Tab1.chains, output_file)
                messagebox.showinfo("Succeed!", "成功保存到%s" % output_file)
                return
            else:
                # 没有勾选，直接转换单个文件为pdbqt文件
                output_file = output_path + os.sep + "preped.pdbqt"
                prepare_receptor(input_file, output_file, fix_method, preserve_charges, nphs, lps, waters, nonstdres)
                messagebox.showinfo("成功", "成功准备受体！\n注意：自动准备会删除DNA等非标准残基，结果仅供参考。")
                return
        else:
            messagebox.showinfo("错误!", "不支持输入内容，请确定是文件夹或者pdb文件")
            return

    def extract_ligand(self, event):
        receptor = self.choose_raw_receptor_entry.textvariable.get()  # 获取受体
        self.output_path = self.ligand_save_path_entry.textvariable.get()  # 配体输出路径

        if not receptor.endswith(".pdb"):
            messagebox.showerror("错误！", "只支持单个pdb格式的受体！")
            return
        if Check.check_path(receptor):
            messagebox.showerror("错误", "受体路径不能包含空格！")
            return
        if Check.check_path(self.output_path):
            messagebox.showerror("错误", "配体输出路径不能包含空格！")
            return
        if not os.path.exists(receptor):
            messagebox.showerror("错误", "所选文件或者文件夹不存在!")
            return
        self._extract_ligand(receptor)

    def _extract_ligand(self, pdb):
        self.structure = ReceptorProcessor.get_structure(pdb)

        top = STopLevel(self.root, 300, 250, "提取配体").toplevel

        # 创建切换卡
        self.notebook = Notebook(top)

        # 创建每个选项卡
        self.choose_model_tab = Frame(self.notebook)
        self.choose_chain_tab = Frame(self.notebook)
        self.choose_ligand_tab = Frame(self.notebook)

        # 添加选项卡
        self.notebook.add(self.choose_model_tab, text="model")
        self.notebook.add(self.choose_chain_tab, text="chain")
        self.notebook.add(self.choose_ligand_tab, text="ligand")

        # 选项卡创建内容
        self.choose_model()
        self.choose_chain()
        self.choose_ligand()

        self.notebook.place(x=10, y=10, width=290, height=230)

    def jump_model(self, event):

        # 禁用后两个
        self.notebook.tab(1, state="disable")
        self.notebook.tab(0, state="normal")
        self.notebook.tab(2, state="disable")

        self.notebook.select(tab_id=0)

    def choose_model(self):
        # 禁用后两个
        self.notebook.tab(1, state="disable")
        self.notebook.tab(2, state="disable")

        self.model_list = Listbox(self.choose_model_tab, width=30, height=10)

        model_ids = ReceptorProcessor.get_model_ids(self.structure)
        Tab1.refresh_listbox(model_ids, self.model_list)

        self.model_list.place(x=10, y=10, width=255, height=150)
        scroll = Scrollbar(self.model_list)
        scroll.pack(side=RIGHT, fill=Y)
        self.model_list.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.model_list.yview)

        next_button = SButton(self.choose_model_tab, "下一步", 165, 170)
        next_button.button.bind("<Button-1>", self.jump_chain)

    def jump_chain(self, event):
        self.model_name = self.model_list.get(ACTIVE)
        model = self.structure[self.model_name]
        chain_names = ReceptorProcessor.get_chain_ids(model)
        Tab1.refresh_listbox(chain_names, self.chain_list)

        # 禁用后两个
        self.notebook.tab(0, state="disable")
        self.notebook.tab(1, state="normal")
        self.notebook.tab(2, state="disable")

        self.notebook.select(tab_id=1)

    def choose_chain(self):
        self.chain_list = Listbox(self.choose_chain_tab, width=30, height=10)
        self.chain_list.place(x=10, y=10, width=255, height=150)
        scroll = Scrollbar(self.chain_list)
        scroll.pack(side=RIGHT, fill=Y)
        self.chain_list.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.chain_list.yview)

        pre_button = SButton(self.choose_chain_tab, "上一步", 10, 170)
        pre_button.button.bind("<Button-1>", self.jump_model)

        next_button = SButton(self.choose_chain_tab, "下一步", 165, 170)
        next_button.button.bind("<Button-1>", self.jump_ligand)

    def jump_ligand(self, event):
        self.chain_name = self.chain_list.get(ACTIVE)
        chain = self.structure[self.model_name][self.chain_name]
        het_names = ReceptorProcessor.get_het_ids(chain)
        Tab1.refresh_listbox(het_names, self.ligand_list)

        # 禁用两个
        self.notebook.tab(0, state="disable")
        self.notebook.tab(2, state="normal")
        self.notebook.tab(1, state="disable")

        self.notebook.select(tab_id=2)

    def choose_ligand(self):
        self.ligand_list = Listbox(self.choose_ligand_tab, width=30, height=10)
        self.ligand_list.place(x=10, y=10, width=255, height=150)
        scroll = Scrollbar(self.ligand_list)
        scroll.pack(side=RIGHT, fill=Y)
        self.ligand_list.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.ligand_list.yview)

        pre_button = SButton(self.choose_ligand_tab, "上一步", 10, 170)
        pre_button.button.bind("<Button-1>", self.jump_chain)

        next_button = SButton(self.choose_ligand_tab, "提取配体", 165, 170)
        create_tooltip(next_button.button, "提取选中的配体为pdbqt格式")
        next_button.button.bind("<Button-1>", self.save_ligand)

    def save_ligand(self, event):
        self.ligand_name = self.ligand_list.get(ACTIVE)

        if not Check.check_python(Configer.get_para("python_path")):
            return

        LigandExtractor(self.structure, self.model_name,
                        self.chain_name, self.ligand_name).extract_ligand(self.output_path)

        input_ligand = self.output_path + os.sep + "%s_%s.pdb" % (self.chain_name, self.ligand_name)
        output_ligand = self.output_path + os.sep + "%s_%s.pdbqt" % (self.chain_name, self.ligand_name)
        pdb_mol2_2_pdbqt(input_ligand, output_ligand)
        os.remove(input_ligand)
        messagebox.showinfo("提取成功！", "成功提取配体！")

    @staticmethod
    def refresh_listbox(content_list: list, list_box: Listbox):
        list_box.delete(0, END)
        for content in content_list:
            list_box.insert(END, content)

    def getinfo(self, event):
        # 获取受体
        receptor = self.choose_raw_receptor_entry.textvariable.get()

        if not receptor.endswith(".pdb"):
            messagebox.showerror("错误！", "只支持查看单个pdb格式的文件信息！")
            return
        if Check.check_path(receptor):
            messagebox.showerror("错误", "受体路径不能包含空格！")
            return
        if not os.path.exists(receptor):
            messagebox.showerror("错误", "所选文件或者文件夹不存在!")
            return

        structure = ReceptorProcessor.get_structure(receptor)

        window = STopLevel(self.root, 500, 400, "PDB信息").toplevel
        wrap_length = 480

        s_name = structure.header["name"]
        SLabel(window, "受体名称:\n" + s_name, 10, 10).label.configure(wraplength=wrap_length)

        s_redate = structure.header["release_date"]
        SLabel(window, "发布时间:\n" + s_redate, 10, 70).label.configure(wraplength=wrap_length)

        s_method = structure.header["structure_method"]
        SLabel(window, "方法:\n" + s_method, 10, 130).label.configure(wraplength=wrap_length)

        s_resolution = str(structure.header["resolution"])
        SLabel(window, "分辨率:\n" + s_resolution + "埃", 10, 190).label.configure(wraplength=wrap_length)

        s_refe = structure.header["journal_reference"]
        reference = SLabel(window, "参考文献:\n" + s_refe, 10, 250).label
        reference.configure(wraplength=wrap_length)
        doi_url = "http://www.doi.org/" + s_refe.strip().split(" ")[-1]
        open_url_button = SButton(window, "打开文献网页", 75, 245)
        open_url_button.button.configure(command=lambda: webbrowser.open(doi_url))
        create_tooltip(open_url_button.button, "使用默认浏览器打开文献链接")

    def create_download_receptor(self):
        # frame创建
        download_receptor_labelframe = LabelFrame(self.root, text="下载受体")
        download_receptor_labelframe.place(x=LEFT_X, y=LEFT_Y,
                                           width=FULL_NOTEBOOK_WIDTH, height=TAB1_LABEL_FRAME_HEIGHT)

        # 第一排，输入pdbid
        SLabel(download_receptor_labelframe, "PDBID：", x=LEFT_X, y=0)
        self.pdb_id_entry = SEntry(download_receptor_labelframe, textvariable=StringVar(),
                                   text=Configer.get_para("pdbid"),
                                   x=70, y=0, width=50)
        create_tooltip(self.pdb_id_entry.entry, "请输入四位PDB的ID")

        # 第二排，保存位置
        pdb_save_path_button = SButton(download_receptor_labelframe,
                                       text="选择保存的路径", x=LEFT_X, y=30)
        create_tooltip(pdb_save_path_button.button, "选择下载受体要保存的位置")
        self.pdb_save_path_entry = SEntry(download_receptor_labelframe,
                                          textvariable=StringVar(),
                                          text=Configer.get_para("pdb_path"),
                                          x=110, y=34, width=440)
        create_tooltip(self.pdb_save_path_entry.entry, "文件将要保存的目录，不存在将创建文件夹")
        pdb_save_path_button.bind_open_dir(entry_text=self.pdb_save_path_entry.textvariable,
                                           title="选择要保存的路径")

        # 第三排，开始下载
        download_pdb_button = SButton(download_receptor_labelframe,
                                      text="开始下载", x=LEFT_X, y=60)
        create_tooltip(download_pdb_button.button, "从Protein Data Bank下载受体")
        download_pdb_button.button.bind("<Button-1>", self.download_pdb)
        self.download_progressbar = Progressbar(download_receptor_labelframe, mode="determinate")
        self.download_progressbar.place(x=100, y=62, width=380)
        create_tooltip(self.download_progressbar, "下载进度")

        self.download_state_label = SLabel(download_receptor_labelframe,
                                           text="没有下载", x=490, y=60)

    def download_pdb(self, event):
        pdb_id = self.pdb_id_entry.textvariable.get()
        file_path = self.pdb_save_path_entry.textvariable.get()
        if len(pdb_id) != 4:
            messagebox.showerror("错误！", "请输入四位pdb代码！")
            return
        state, current_entry = check_pdb_status(pdb_id)
        if state == "CURRENT":
            self._download_pdb(current_entry, file_path)
        elif state == "OBSOLETE":
            messagebox.showwarning("当前pdb已经过时！", "将下载%s" % current_entry)
            self._download_pdb(current_entry, file_path)
        else:
            messagebox.showerror("错误！", "当前pdb不存在，请检查id是否正确！")
            return

    def _download_pdb(self, pdb_id, file_path):
        url = 'http://www.rcsb.org/pdb/files/%s.pdb' % pdb_id

        # 末尾如果含有斜杠，去掉斜杠
        if file_path.endswith(os.sep):
            file_path = file_path[0:-1]

        if not os.path.exists(file_path):
            os.mkdir(file_path)

        filename = file_path + os.sep + "%s.pdb" % pdb_id

        try:
            file_size = len(requests.get(url).content)
        except requests.HTTPError:
            messagebox.showerror("下载错误", "请求失败，请重试")
            return
        except:
            messagebox.showerror("下载错误", "请求失败，请重试")
            return

        self.download_progressbar["maximum"] = file_size

        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024  # 单次请求最大值
            data_length = 0
            with open(filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    data_length += len(data)
                    # 更新进度条
                    self.download_progressbar["value"] = data_length
                    self.download_progressbar.update()

                    # 更新标签
                    percent = int(data_length / file_size * 100)
                    self.download_state_label.label.configure(text="%i/100" % percent)
                    self.download_state_label.label.update()

        # 文件下载结束
        messagebox.showinfo("下载成功！", "成功下载%s" % pdb_id)

        # 更新进度条
        self.download_progressbar["value"] = 0
        self.download_progressbar.update()

        # 更新标签
        self.download_state_label.label.configure(text="没有任务")
        self.download_state_label.label.update()

    def save_para(self):
        self.configer.para_dict["pdbid"] = self.pdb_id_entry.textvariable.get()
        self.configer.para_dict["pdb_path"] = self.pdb_save_path_entry.textvariable.get()
        self.configer.para_dict["extract_ligand_path"] = self.ligand_save_path_entry.textvariable.get()
        self.configer.para_dict["raw_receptor_path"] = self.choose_raw_receptor_entry.textvariable.get()
        self.configer.para_dict["preped_path"] = self.choose_prepare_output_path.textvariable.get()
        self.configer.para_dict["fix_receptor"] = self.is_fix_receptor.variable.get()
        self.configer.para_dict["fix_method"] = self.fix_method.textvariable.get()
        self.configer.para_dict["preserve_charges"] = self.preserve_charges.variable.get()
        self.configer.para_dict["nphs"] = self.nphs.variable.get()
        self.configer.para_dict["lps"] = self.lps.variable.get()
        self.configer.para_dict["waters"] = self.waters.variable.get()
        self.configer.para_dict["nonstdres"] = self.nonstdres.variable.get()
