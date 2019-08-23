from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from tools.text import *
from tools.number import *
from tools.configer import Configer

from sail_widget.tooltip import create_tooltip
from sail_widget.tab1 import Tab1


class MainWindows(object):

    def __init__(self):
        # 初始化
        self.main_window = Tk()

        # 参数保存工具
        self.config = Configer()
        self.tab1_configer = None

        # 如果第一次打开，创建参数文件
        Configer.first_open()

        # 窗口初始化
        self.init_window()

        # 创建切换卡
        self.create_notebook()

        # 三方程序配置
        self.create_config_button()

        # 退出按钮
        self.create_exit_button()

        # 点击x退出
        self.main_window.protocol("WM_DELETE_WINDOW", self.save_para)

    def create_config_button(self):
        # 脚本配置
        config_button = Button(self.main_window, text="脚本配置")
        config_button.place(x=CONFIG_BUTTON_X, y=CONFIG_BUTTON_Y, width=BUTTON_WIDTH)
        create_tooltip(config_button, "设置脚本所需路径")

    def create_exit_button(self):
        """
        创建退出按钮
        """
        exit_button = Button(self.main_window, text="退出", command=self.save_para)
        exit_button.place(x=EXIT_BUTTON_X, y=EXIT_BUTTON_Y, width=BUTTON_WIDTH)
        create_tooltip(exit_button, "保存参数并退出软件")

    def init_window(self):
        """
        添加标题，禁用窗口缩放，显示居中。
        """
        # 标题
        self.main_window.title(WINDOWS_TITLE)

        # 禁用窗口缩放
        self.main_window.resizable(width=False, height=False)

        # 窗口居中显示
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x = (screen_width / 2) - (MAIN_WINDOWS_WIDTH / 2)
        y = (screen_height / 2) - (MAIN_WINDOWS_HEIGHT / 2)
        self.main_window.geometry('%dx%d+%d+%d' % (MAIN_WINDOWS_WIDTH, MAIN_WINDOWS_HEIGHT, x, y))

    def create_notebook(self):
        # 大框架
        notebook = Notebook()

        # 准备受体
        tab1 = Frame(notebook)

        # 准备对接配置
        tab2 = Frame(notebook)

        # 准备配体
        tab3 = Frame(notebook)

        # 分子对接
        tab4 = Frame(notebook)

        # 提取分数
        tab5 = Frame(notebook)

        # 生成复合物
        tab6 = Frame(notebook)

        # 关于
        tab7 = Frame(notebook)

        # 放置选项卡
        notebook.add(tab1, text=TAB1_TEXT)
        notebook.add(tab2, text=TAB2_TEXT)
        notebook.add(tab3, text=TAB3_TEXT)
        notebook.add(tab4, text=TAB4_TEXT)
        notebook.add(tab5, text=TAB5_TEXT)
        notebook.add(tab6, text=TAB6_TEXT)
        notebook.add(tab7, text=TAB7_TEXT)

        # 默认显示卡
        notebook.select(tab_id=DEFAULT_TAB)

        # 禁用某一个选项卡
        # self.notebook.tab(1, state="disable")

        # 放置切换卡
        notebook.place(x=NOTEBOOK_X, y=NOTEBOOK_Y,
                       width=NOTEBOOK_WIDTH, height=NOTEBOOK_HEIGHT)

        # 选项卡内容
        self.tab1_configer = Tab1(tab1, self.config)

    def save_para(self):
        if messagebox.askokcancel("退出", "保存参数并退出软件？"):
            self.config.para_dict["python_path"] = self.config.get_para("python_path")
            self.config.para_dict["obabel_path"] = self.config.get_para("obabel_path")
            self.tab1_configer.save_para()
            self.config.save_para()
            self.main_window.destroy()


if __name__ == '__main__':
    mw = MainWindows()
    mw.main_window.mainloop()
