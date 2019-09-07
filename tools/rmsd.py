# 计算两个pdb文件的rmsd
# 根据wiki，RMSD等于1/N的所有原子距离的平方和的平方根
# 即根号1/N[(X1-X1')^2+(Y1-Y1')^2+(Z1-Z1')^2+(XN-XN')^2+(YN-YN')^2+(ZN-ZN')^2..]
import os

from tools.file_processor import get_backbone, get_ligand_position
from tools.file_path import cal_rmsd_path


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


def charnley_cal_rmsd(file1, file2, rotation_method, reorder_method):
    """
    使用charnley方法计算rmsd
    :param outputfile: 输出文件
    :param file1: 第一个xyz文件
    :param file2: 第二个xyz文件
    :param rotation_method: 是否旋转原子。kabsch, quaternion or none
    :param reorder_method: 对齐原子。hungarian, brute, distance
    :return 成功返回rmsd值，不成功返回False
    """
    cmd = ""
    # 情况一：不旋转
    if rotation_method == "none":
        cmd = "python %s %s %s -e --reorder-method %s" % (cal_rmsd_path, file1, file2, reorder_method)

    # 情况二：旋转
    else:
        cmd = "python %s %s %s -r %s -e --reorder-method %s" % (cal_rmsd_path, file1, file2,
                                                                rotation_method, reorder_method)
    rmsd = os.popen(cmd).read()
    return rmsd


if __name__ == '__main__':
    print(cal_rmsd(r"D:\Desktop\toptecam_out1_1.pdb", r"D:\Desktop\cystal.pdb"))
