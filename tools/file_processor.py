import os
import shutil
import copy

from tools.configer import Configer


def pdbqt2dir(pdbqt_path):
    """
    在相同路径创建一个该名字的文件夹，将pdbqt文件移动进去。\n
    比如pdbqt_path = ./Proteins/a.pdbqt
    :param pdbqt_path: pdbqt文件路径
    """
    # 1.创建文件夹
    pdbqt_dir = pdbqt_path[0:-6]
    os.mkdir(pdbqt_dir)
    # 2.移动文件
    target_path = pdbqt_dir + os.sep + "preped.pdbqt"
    shutil.move(pdbqt_path, target_path)


def gen_config_file(output_name, x, y, z, size):
    """
    根据x,y,z,size生成config文件
    :param output_name: 输出路径文件名
    :param x: x坐标
    :param y: y坐标
    :param z: z坐标
    :param size: 盒子大小
    """
    exhaustiveness = Configer.get_para("exhaustiveness") if Configer.get_para("exhaustiveness") != "" else 8
    num_modes = Configer.get_para("num_modes") if Configer.get_para("num_modes") != "" else 9
    energy_range = Configer.get_para("energy_range") if Configer.get_para("energy_range") != "" else 3
    with open(output_name, "w") as f:
        f.writelines("center_x = " + str(x) + "\n")
        f.writelines("center_y = " + str(y) + "\n")
        f.writelines("center_z = " + str(z) + "\n")
        f.writelines("size_x = " + str(size) + "\n")
        f.writelines("size_y = " + str(size) + "\n")
        f.writelines("size_z = " + str(size) + "\n")
        f.writelines("exhaustiveness = " + exhaustiveness + "\n")
        f.writelines("num_modes = " + num_modes + "\n")
        f.writelines("energy_range = " + energy_range + "\n")


def get_config_files(protein_path):
    """
    获取一个路径中的config文件
    :param protein_path: 蛋白文件夹路径，比如"./Proteins/01"
    :return: 蛋白的config文件列表
    """
    files = os.listdir(protein_path)
    config_files = []
    for file in files:
        if file.startswith("config"):
            config_files.append(protein_path + os.sep + file)
    return config_files


def mk_output_dir(file_path):
    """
    如果不存在就创建输出文件夹
    :param file_path: 目标文件夹
    """
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def create_scores_file(output_file, scores_dict):
    """
    创建分数文件
    :param output_file: 输出目录
    :param scores_dict:分数字典
    """
    with open(output_file, "w") as f:
        f.write("receptor_name\tligand_name\tscores\n")
        for receptor in scores_dict:
            for ligand in scores_dict[receptor]:
                f.write(receptor + "\t" + ligand + "\t" + scores_dict[receptor][ligand] + "\n")


def get_best_scores(scores_dict):
    """
    传入分数字典，将分数最小的输出，多个都输出。
    :param scores_dict: 分数列表
    :return: 最小的配体字典
    """
    # 获取分数最低的值
    tmp_dict = copy.deepcopy(scores_dict)
    for receptor in scores_dict:
        min_score = 0
        for ligand in scores_dict[receptor]:
            score = float(scores_dict[receptor][ligand])
            if score <= min_score:
                min_score = score

        for ligand in scores_dict[receptor]:
            if float(scores_dict[receptor][ligand]) > min_score:
                # 删除分数大于最小值的字典
                tmp_dict[receptor].pop(ligand)

    return tmp_dict


if __name__ == '__main__':
    pass
    # 本地调试代码
    # pdbqt2dir("./Proteins/pdb (1).pdbqt")
    # gen_config_file("./config.txt", 1, 1, 1, 20)
    # get_config_files(r".\Proteins\01")
    # r_dict = {'01': {'0.pdbqt': '-3.2', '1.pdbqt': '-3.1', '2.pdbqt': '-3.5'},
    #           '02': {'0.pdbqt': '-3.2', '1.pdbqt': '-3.2', '2.pdbqt': '-3.2'}}
    # print(get_best_scores(r_dict))
