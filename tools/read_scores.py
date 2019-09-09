import os
import sys

from tools.file_processor import create_scores_file
from tools.file_processor import get_best_scores


def read_root_folder_scores(output_root_folder_path, mode=0):
    """
    读取根文件夹中的所有分数。根文件夹包含受体名文件夹，受体文件夹下面是配体
    :param output_root_folder_path: 含有受体文件夹的文件夹
    :param mode: 分数模式，默认输出所有分数，相应数字输出第x个分数。
    :return: 受体和受体中文件和分数的字典。
    """
    receptor_dict = {}
    receptors = os.listdir(output_root_folder_path)
    for receptor in receptors:
        path = output_root_folder_path + os.sep + receptor
        if os.path.isdir(path):
            score_dict = read_folder_scores(path, mode)
            receptor_dict[receptor] = score_dict

    return receptor_dict


def read_folder_scores(output_folder_path, mode=0):
    """
    读取一个文件夹中所有文件的所有分数
    :param output_folder_path: 需要读取的文件夹，其中包含输出的配体文件
    :param mode: 分数模式，默认输出所有分数，相应数字输出第x个分数。
    :return: 文件名和分数的字典
    """
    scores_dict = {}
    ligands = os.listdir(output_folder_path)
    for ligand in ligands:
        if ligand.endswith(".pdbqt"):
            path = output_folder_path + os.sep + ligand
            scores = read_scores(path)
            if len(scores) == 0:
                continue
            if mode == 0:
                scores_dict[ligand] = scores
            elif mode <= len(scores):
                scores_dict[ligand] = scores[mode - 1]
            else:
                scores_dict[ligand] = scores[-1]

    return scores_dict


def read_scores(output_file_path):
    """
    读取一个文件的所有分数
    :param output_file_path: vina对接的输出文件
    :return: 所有分数的合集
    """
    scores = []
    with open(output_file_path, "r") as f:
        for line in f.readlines():
            if line.startswith("REMARK VINA RESULT"):
                scores.append(line.split()[3])

    return scores


if __name__ == '__main__':
    # 读取命令行输入
    if len(sys.argv) == 1:
        print("--------------------------------------------------------------------------------")
        print('命令格式:\n'
              'python .\\read_scores.py 对接结果输出根目录 结果输出目录\n\n'
              '其中:\n'
              '对接结果输出根目录：对接之后结果所在的目录，比如..\\Output\n'
              '结果输出目录:输出txt文件的位置，比如..\\Output')
        print("--------------------------------------------------------------------------------")
        sys.exit()
    elif len(sys.argv) != 3:
        print("参数个数不正确，请检查参数！")
        sys.exit()
    else:
        re_dict = read_root_folder_scores(sys.argv[1], mode=1)
        best_dict = get_best_scores(re_dict)
        create_scores_file(sys.argv[2] + os.sep + "scores.txt", best_dict)
