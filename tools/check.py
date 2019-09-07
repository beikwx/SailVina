from tkinter import messagebox

from tools.file_path import *
from tools.configer import Configer


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
        if Configer.get_para("obabel_path") != "":
            return True
        if obabel_path.count(" ") > 0 or not obabel_path.endswith("obabel.exe"):
            messagebox.showerror("输入错误！", "obabel.exe选择不正确！请确保路径不包含空格并且是obabel.exe文件！")
            return False
        obabel_cmd = os.popen(obabel_path).read()
        # print(obabel_cmd)
        if "Usage:\nobabel" not in obabel_cmd:
            messagebox.showerror("错误！", "obabel.exe不正确，请在“脚本配置”中选择！")
            return False
        messagebox.showinfo("obabel配置成功！", "obabel配置成功！")
        return True

    @staticmethod
    def check_python(choose_python_path):
        """
        检查adt的python路径是否配置正确
        :param choose_python_path: 选择的python路径
        :return: 正确返回True
        """
        # 如果有内容，直接判断通过
        if Configer.get_para("python_path") != "":
            return True
        if choose_python_path.count(" ") > 0 or not choose_python_path.endswith("python.exe"):
            messagebox.showerror("输入错误！", "adt的python.exe选择不正确，请确保路径不包含空格并且是python.exe文件！")
            return False
        check_cmd = "%s %s" % (choose_python_path, pdbqt_to_pdb_path)
        state = os.system(check_cmd)
        if state == 1:
            messagebox.showerror("python路径错误！", "请确定选择的是安装adt软件的python.exe！")
            return False
        messagebox.showinfo("python配置成功！", "python配置成功！")
        return True

    @staticmethod
    def check_path(text: str):
        """
        检查路径，不为空，没有空格
        :param text: 路径名
        :return: 都没有返回真
        """
        if text == "" or Check.has_space(text):
            return True
        return False

    @staticmethod
    def check_config(dir_path):
        """
        判断一个路径中是否有config文件。名字包含config即可
        :param dir_path: 含有config.txt等的文件夹
        :return: 如果有，返回真
        """
        filenames = os.listdir(dir_path)
        for filename in filenames:
            if "config" in filename:
                return True
        else:
            return False

    @staticmethod
    def check_file(filename):
        """

        :param filename: 判断的名字
        :return: 是文件返回1，不是返回0。文件不存在返回0
        """
        if os.path.isfile(filename):
            if os.path.exists(filename):
                return 1
            else:
                print(filename + "不存在")
                return 0
        else:
            print(filename + "不是文件")
            return 0

    @staticmethod
    def path_has_pdbqt(file_path):
        """
        判断一个路径中是否有pdbqt文件
        :param file_path: 文件路径
        :return: 有返回真，没有返回False
        """
        files = os.listdir(file_path)
        for file in files:
            if file.endswith(".pdbqt"):
                return True
        else:
            return False

    @staticmethod
    def next_path_has_pdbqt(file_path):
        """
        判断该路径下某个文件夹中含有pdbqt文件
        :param file_path: 路径
        :return: 有返回True，没有返回False
        """
        files = os.listdir(file_path)
        for file in files:
            next_dir = os.path.join(file_path, file)
            if os.path.isdir(next_dir):
                if Check.path_has_pdbqt(next_dir):
                    return True
        else:
            return False


if __name__ == '__main__':
    print(Check.check_config(r"D:\Vina_Dock\Proteins"))
