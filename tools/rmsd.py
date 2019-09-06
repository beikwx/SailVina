# 计算两个pdb文件的rmsd
# 根据wiki，RMSD等于1/N的所有原子距离的平方和的平方根
# 即根号1/N[(X1-X1')^2+(Y1-Y1')^2+(Z1-Z1')^2+(XN-XN')^2+(YN-YN')^2+(ZN-ZN')^2..]
from tools.file_processor import get_backbone, get_ligand_position
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


def charnley_cal_rmsd(file1, file2, rotation, reorder_method, outputfile):
    """
    使用charnley方法计算rmsd
    :param outputfile: 输出文件
    :param file1: 第一个xyz文件
    :param file2: 第二个xyz文件
    :param rotation: 是否旋转原子。kabsch, quaternion or none
    :param reorder_method: 对齐原子。hungarian, brute, distance
    :return 是否成功
    """

    # 第一步
    p_all_atoms, p_all = get_coordinates(file1, "xyz")
    q_all_atoms, q_all = get_coordinates(file2, "xyz")

    # 第二步
    p_size = p_all.shape[0]
    q_size = q_all.shape[0]
    if not p_size == q_size:
        print("错误！%s和%s的原子数不一样！" % (file1, file2))
        return False
    if np.count_nonzero(p_all_atoms != q_all_atoms) and not reorder_method:
        print("%s和%s原子顺序不一样！请尝试使用reorder方法！" % (file1, file2))
        return False

    # Set local view
    p_view = None
    q_view = None

    # Set local view
    if p_view is None:
        p_coord = copy.deepcopy(p_all)
        q_coord = copy.deepcopy(q_all)
        p_atoms = copy.deepcopy(p_all_atoms)
        q_atoms = copy.deepcopy(q_all_atoms)

    else:

        if args.reorder and args.output:
            print("error: Cannot reorder atoms and print structure, when excluding atoms (such as --no-hydrogen)")
            quit()

        if args.use_reflections and args.output:
            print("error: Cannot use reflections on atoms and print, when excluding atoms (such as --no-hydrogen)")
            quit()

        p_coord = copy.deepcopy(p_all[p_view])
        q_coord = copy.deepcopy(q_all[q_view])
        p_atoms = copy.deepcopy(p_all_atoms[p_view])
        q_atoms = copy.deepcopy(q_all_atoms[q_view])


if __name__ == '__main__':
    print(cal_rmsd(r"D:\Desktop\toptecam_out1_1.pdb", r"D:\Desktop\cystal.pdb"))
