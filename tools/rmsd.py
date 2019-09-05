# 计算两个pdb文件的rmsd
# 根据wiki，RMSD等于1/N的所有原子距离的平方和的平方根
# 即根号1/N[(X1-X1')^2+(Y1-Y1')^2+(Z1-Z1')^2+(XN-XN')^2+(YN-YN')^2+(ZN-ZN')^2..]
from tools.file_processor import get_backbone, get_ligand_position


def cal_rmsd(file1, file2):
    """
    计算两个文件的rmsd，目前只支持pdb文件
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


if __name__ == '__main__':
    print(cal_rmsd(r"D:\Desktop\toptecam_out1_1.pdb", r"D:\Desktop\cystal.pdb"))
