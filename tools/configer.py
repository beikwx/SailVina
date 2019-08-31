import os

from tools.file_path import para_file


class Configer(object):

    def __init__(self):
        self.para_dict = {}

    @staticmethod
    def first_open():
        """
        如果第一次打开该软件，创建para.txt文件
        """
        if not os.path.exists(para_file):
            with open(para_file, "w") as f:
                initial_value = "center_x=0.0\n" \
                                "center_y=0.0\n" \
                                "center_z=0.0\n" \
                                "size_x=0.0\n" \
                                "size_y=0.0\n" \
                                "size_z=0.0\n" \
                                "exhaustiveness=8\n" \
                                "num_modes=9\n" \
                                "energy_range=3\n" \
                                "gen3d=1\n" \
                                "pH=7.4\n" \
                                "is_minimize=1\n" \
                                "docking_times=1\n" \
                                "complex_ligand_num=1\n" \
                                "remain_ligand=0\n" \
                                "fix_receptor=0\n" \
                                "fix_method=None\n" \
                                "preserve_charges=0\n" \
                                "nphs=1\n" \
                                "lps=1\n" \
                                "waters=1\n" \
                                "nonstdres=1\n"
                f.write(initial_value)

    @staticmethod
    def get_para(para_text):
        if not os.path.exists(para_file):
            return ""
        with open(para_file, "r") as f:
            for line in f.readlines():
                if line.split("=")[0] == para_text:
                    return str(line.split("=")[1].strip())
            else:
                return ""

    def save_para(self):
        with open(para_file, "w") as f:
            for para in self.para_dict:
                f.write("%s=%s\n" % (para, self.para_dict[para]))


class ConfigReader(object):
    @staticmethod
    def get_config_para(parameter):
        if parameter == "\n":
            return "", ""
        return parameter.split("=")[0].strip(), parameter.split("=")[1].strip()


class ConfigWriter(object):

    @staticmethod
    def write_config(para_dict, output_path):
        with open("%s" % output_path + os.sep + "config.txt", "w") as f:
            for para in para_dict:
                line = "%s %s\n" % (para, para_dict[para])
                f.writelines(line)
