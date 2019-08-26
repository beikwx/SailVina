from tools.configer import Configer
from tools.file_path import *

obabel_path = Configer.get_para("obabel_path")
python_path = Configer.get_para("python_path")


def pdb_2_other(input_file, output_file):
    """
    使用obabel将pdb文件转换为其他文件
    :param input_file: 输入的pdb文件
    :param output_file: 输出的其他格式文件
    :return 执行结果
    """
    cmd = "%s %s -O %s" % (obabel_path, input_file, output_file)
    convert_result(cmd, output_file)


def pdbqt_2_pdb(input_file, output_file):
    """
    使用adt将pdbqt文件转pdb文件
    :param input_file: 输入的pdbqt文件
    :param output_file: 输出的pdb文件
    """
    cmd = "%s %s -f %s -o %s" % (python_path, pdbqt_to_pdb_path,
                                 input_file, output_file)
    convert_result(cmd, output_file)


def pdb_mol2_2_pdbqt(input_file, output_file):
    """
    使用adt将pdb或者mol2文件转pdbqt
    :param input_file: 输入的pdb或者mol2文件
    :param output_file: 输出文件
    """
    cmd = "%s %s -l %s -o %s" % (python_path, prepare_ligand4_path,
                                 input_file, output_file)
    convert_result(cmd, output_file)


def two_d_2_pdb(input_file, output_file, ph, minimize):
    """
    使用obabel将2d文件转换为pdb文件
    :param input_file: 输入的2d格式文件。mol，smi。
    :param output_file: 输入文件
    :param ph: 加氢的ph值
    :param minimize: 最小化方法
    """
    cmd = "%s %s -O %s -p %s --gen3d --minimize --ff %s" % (obabel_path, input_file, output_file, ph, minimize)
    convert_result(cmd, output_file)


def three_d_2_pdb(input_file, output_file, is_minimize, minimize):
    """
    使用ob将3d文件转为pdb文件
    :param input_file: 3d文件。sdf
    :param output_file: 输出文件
    :param is_minimize: 是否能量最小化
    :param minimize: 最小化方法
    """
    if is_minimize == "1":
        cmd = "%s %s -O %s --minimize --ff %s" % (obabel_path, input_file, output_file, minimize)
        convert_result(cmd, output_file)
    else:
        ob(input_file, output_file)


def ob_3d_min(input_file, output_file, ph, minimize):
    two_d_2_pdb(input_file, output_file, ph, minimize)


def ob_3d(input_file, output_file, ph):
    cmd = "%s %s -O %s -p %s --gen3d" % (obabel_path, input_file, output_file, ph)
    convert_result(cmd, output_file)


def ob_min(input_file, output_file, ph, minimize):
    cmd = "%s %s -O %s -p %s --minimize --ff %s" % (obabel_path, input_file, output_file, ph, minimize)
    convert_result(cmd, output_file)


def ob(input_file, output_file):
    cmd = "%s %s -O %s" % (obabel_path, input_file, output_file)
    convert_result(cmd, output_file)


def convert_result(cmd, output_file):
    """
    执行命令，并查看是否成功
    :param cmd: 命令
    :param output_file:输出文件
    """
    exit_code = os.system(cmd)
    if exit_code == 0:
        print("------------------------------------------------------------")
        print("%s转换成功" % output_file)
        print("------------------------------------------------------------")
    else:
        print("------------------------------------------------------------")
        print("%s准备失败，可能文件内部格式有误" % output_file)
        print("------------------------------------------------------------")
