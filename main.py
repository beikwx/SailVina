from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from tools.text import *
from tools.number import *
from tools.configer import Configer

from sail_widget.tooltip import create_tooltip
from sail_widget.tab1 import Tab1
from sail_widget.tab2 import Tab2
from sail_widget.tab3 import Tab3
from sail_widget.tab4 import Tab4
from sail_widget.tab5 import Tab5
from sail_widget.tab6 import Tab6
from sail_widget.tab7 import Tab7
from sail_widget.addition_tools_tab import AdditionToolsTab
from sail_widget.set_config import SetConfig


class MainWindows(object):

    def __init__(self):
        # 初始化
        self.main_window = Tk()

        # 参数保存工具
        self.config = Configer()
        self.tab1_configer = None
        self.tab2_configer = None
        self.tab3_configer = None
        self.tab4_configer = None
        self.tab5_configer = None
        self.tab6_configer = None
        self.tab7_configer = None
        self.tab8_configer = None

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
        config_button = Button(self.main_window, text="脚本配置", command=self.set_config)
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

        # 工具
        tab5 = Frame(notebook)

        # 生成复合物
        tab6 = Frame(notebook)

        # 关于
        tab7 = Frame(notebook)

        # 其他工具
        tab8 = Frame(notebook)

        # 放置选项卡
        notebook.add(tab1, text=TAB1_TEXT)
        notebook.add(tab2, text=TAB2_TEXT)
        notebook.add(tab3, text=TAB3_TEXT)
        notebook.add(tab4, text=TAB4_TEXT)
        notebook.add(tab5, text=TAB5_TEXT)
        notebook.add(tab8, text=TAB8_TEXT)
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
        self.tab2_configer = Tab2(tab2, self.config)
        self.tab3_configer = Tab3(tab3, self.config)
        self.tab4_configer = Tab4(tab4, self.config)
        self.tab5_configer = Tab5(tab5, self.config)
        self.tab6_configer = Tab6(tab6, self.config)
        self.tab8_configer = AdditionToolsTab(tab8, self.config)
        self.tab7_configer = Tab7(tab7)

    def set_config(self):
        SetConfig(self.main_window, self.config)

    def save_para(self):
        if messagebox.askokcancel("退出", "保存参数并退出软件？"):
            self.config.para_dict["python_path"] = Configer.get_para("python_path")
            self.config.para_dict["obabel_path"] = Configer.get_para("obabel_path")

            # 保存各个标签的参数
            self.tab1_configer.save_para()
            self.tab2_configer.save_para()
            self.tab3_configer.save_para()
            self.tab4_configer.save_para()
            self.tab5_configer.save_para()
            self.tab6_configer.save_para()
            self.tab8_configer.save_para()

            # 进行文件保存
            self.config.save_para()

            # 关闭窗口
            self.main_window.destroy()


if __name__ == '__main__':
    mw = MainWindows()
    mw.main_window.mainloop()
