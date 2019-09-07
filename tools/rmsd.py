# 计算两个pdb文件的rmsd
# 根据wiki，RMSD等于1/N的所有原子距离的平方和的平方根
# 即根号1/N[(X1-X1')^2+(Y1-Y1')^2+(Z1-Z1')^2+(XN-XN')^2+(YN-YN')^2+(ZN-ZN')^2..]
import os

from tools.file_processor import get_backbone, get_ligand_position
from tools.file_processor import mk_output_dir, remove_dir_if_exist
from tools.format_convertor import ob_noh_xyz
from tools.calculate_rmsd import *


def cal_rmsd(file1, file2):
    """
    自己写的，标准的计算两个文件的rmsd，目前只支持pdb文件
    :param file1: 第一个pdb文件
    :param file2: 第二个pdb文件
    :return: rmsd值,-1表示骨架不一样
    """
    # 读取骨架，需要一致
    backbone1 = get_backbone(file1)
    backbone2 = get_backbone(file2)

    if not backbone1 == backbone2:
        print("%s和%s的骨架不一样" % (file1, file2))
        return -1

    file1_position = get_ligand_position(file1)
    file2_position = get_ligand_position(file2)

    # 计算距离平方和
    sum_distance = 0
    i = 0
    while i < len(file1_position):
        distance = pow((file1_position[i][0] - file2_position[i][0]), 2) + \
                   pow((file1_position[i][1] - file2_position[i][1]), 2) + \
                   pow((file1_position[i][2] - file2_position[i][2]), 2)
        sum_distance += distance
        i += 1

    # 除以骨架原子数开根号
    return pow(sum_distance / len(file1_position), 0.5)


def charnley_cal_rmsd(file1, file2, s_rotation_method, s_reorder_method):
    """
    使用稍微修改的charnley方法计算rmsd。对齐原子不会改变原始坐标。
    :param file1: 第一个xyz文件
    :param file2: 第二个xyz文件
    :param s_rotation_method: 是否旋转原子。kabsch, quaternion or none
    :param s_reorder_method: 对齐原子。hungarian, brute, distance
    :return 成功返回rmsd值，不成功返回False
    """
    # 第一步，创建临时文件夹，删除氢原子

    file1_path, file1_name = os.path.split(file1)
    file2_path, file2_name = os.path.split(file2)

    tmp1_dir = os.path.join(file1_path, "no_h_tmp")
    tmp2_dir = os.path.join(file2_path, "no_h_tmp")
    mk_output_dir(tmp1_dir)
    mk_output_dir(tmp2_dir)

    output_file1 = os.path.join(tmp1_dir, file1_name)
    output_file2 = os.path.join(tmp1_dir, file2_name)

    ob_noh_xyz(file1, output_file1)
    ob_noh_xyz(file2, output_file2)

    # 获取原子数和原子坐标
    p_all_atoms, p_all = get_coordinates(output_file1, "xyz")
    q_all_atoms, q_all = get_coordinates(output_file2, "xyz")

    # 判断两个文件原子数是否一致
    p_size = p_all.shape[0]
    q_size = q_all.shape[0]

    if not p_size == q_size:
        print("错误！%s和%s的原子数不一致")
        return False

    p_coord = copy.deepcopy(p_all)
    q_coord = copy.deepcopy(q_all)
    p_atoms = copy.deepcopy(p_all_atoms)
    q_atoms = copy.deepcopy(q_all_atoms)

    # print("p原始原子:\n", p_atoms)
    # print("q原始原子:\n", q_atoms)
    # print("q原始坐标:\n", q_coord)

    rotation_method = None

    # 原子旋转方法
    if s_rotation_method == "kabsch":
        rotation_method = kabsch_rmsd

    elif s_rotation_method == "quaternion":
        rotation_method = quaternion_rmsd

    elif s_rotation_method == "none":
        rotation_method = None

    reorder_method = None

    # 原子对齐方法
    if s_reorder_method == "hungarian":
        reorder_method = reorder_hungarian

    elif s_reorder_method == "brute":
        reorder_method = reorder_brute

    elif s_reorder_method == "distance":
        reorder_method = reorder_distance

    q_review = reorder_method(p_atoms, q_atoms, p_coord, q_coord)
    q_coord = q_coord[q_review]
    q_atoms = q_atoms[q_review]

    if not all(p_atoms == q_atoms):
        print("错误！无法对齐原子！")
        return False

    # print("对齐后q原子\n", q_atoms)
    # print("对齐后q坐标\n", q_coord)
    #
    # xyz = set_coordinates(q_atoms, q_coord, title="{} - modified".format(output_file2))
    # print(xyz)

    if rotation_method is None:
        result_rmsd = rmsd(p_coord, q_coord)
    else:
        result_rmsd = rotation_method(p_coord, q_coord)

    # 删除临时文件
    remove_dir_if_exist(tmp1_dir)
    remove_dir_if_exist(tmp2_dir)

    return "%.4f" % result_rmsd


if __name__ == '__main__':
    # 重新对齐算法不同，可能导致不同C位置不同，产生不同rmsd
    h_rmsd = charnley_cal_rmsd(r"D:\Desktop\01.xyz", r"D:\Desktop\02.xyz", "none", "hungarian")
    # b_rmsd = charnley_cal_rmsd(r"D:\Desktop\01.xyz", r"D:\Desktop\02.xyz", "none", "brute")
    # d_rmsd = charnley_cal_rmsd(r"D:\Desktop\01.xyz", r"D:\Desktop\02.xyz", "none", "distance")

    # 0.9437
    print("hungarian_rmsd:%s" % h_rmsd)

    # 无法计算
    # print("brute_rmsd:%s" % b_rmsd)

    # 1.0301
    # print("distance_rmsd:%s" % d_rmsd)
