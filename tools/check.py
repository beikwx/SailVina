import os
from tkinter import messagebox
from tools.file_path import *


class Check(object):

    @staticmethod
    def has_space(text: str) -> object:
        """

        :param text: 要检测的字符串
        :return:包含空格返回True，不包含空格返回False
        :rtype: bool
        """
        if text.count(" ") > 0:
            return True
        return False

    @staticmethod
    def check_obabel(obabel_path):
        if obabel_path.count(" ") > 0 or not obabel_path.endswith("obabel.exe"):
            messagebox.showerror("输入错误！", "obabel.exe选择不正确！请确保路径不包含空格"
                                          "并且是obabel.exe文件！")
            return False
        obabel_cmd = os.popen(obabel_path).read()
        print(obabel_cmd)
        if "Usage:\nobabel" not in obabel_cmd:
            messagebox.showerror("错误！", "obabel.exe不正确，请在“脚本配置”中选择！")
            return False
        return True

    @staticmethod
    def check_python(python_path):
        if python_path.count(" ") > 0 or not python_path.endswith("python.exe"):
            messagebox.showerror("输入错误！", "adt的python.exe选择不正确，请确保路径不包含空格"
                                          "并且是python.exe文件！")
            return False
        check_cmd = "%s %s" % (python_path, pdbqt_to_pdb_path)
        state = os.system(check_cmd)
        if state == 1:
            messagebox.showerror("python路径错误！", "请确定选择的是安装adt软件的python.exe！")
            return False
        return True

    @staticmethod
    def check_path(text: str):
        if text == "" or Check.has_space(text):
            return True
        return False
