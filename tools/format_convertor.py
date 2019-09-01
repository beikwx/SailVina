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
    """
    进行3d和最小化的格式转换。
    :param input_file: 输入文件
    :param output_file: 输出文件
    :param ph: ph值
    :param minimize:最小化方法
    """
    two_d_2_pdb(input_file, output_file, ph, minimize)


def ob_3d(input_file, output_file, ph):
    cmd = "%s %s -O %s -p %s --gen3d" % (obabel_path, input_file, output_file, ph)
    convert_result(cmd, output_file)


def ob_min(input_file, output_file, ph, minimize):
    cmd = "%s %s -O %s -p %s --minimize --ff %s" % (obabel_path, input_file, output_file, ph, minimize)
    convert_result(cmd, output_file)


def ob(input_file, output_file):
    """
    单纯使用obabel进行格式转换，不进行任何操作
    :param input_file: 输入文件
    :param output_file: 输出文件
    """
    cmd = "%s %s -O %s" % (obabel_path, input_file, output_file)
    convert_result(cmd, output_file)


def smi_2_mol(smi_string, output_file):
    """
    将smi字符串转成mol格式
    :param smi_string: smi字符串
    :param output_file: 输出的mol格式文件
    """
    cmd = '%s -:"%s" -O %s --gen2d' % (obabel_path, smi_string, output_file)
    convert_result(cmd, output_file)


def ob_join(input_file1, input_file2, output_file):
    """
    合并两个文件到一个文件
    :param input_file1: 第一个文件
    :param input_file2: 第二个文件
    :param output_file: 输出文件
    """
    cmd = "%s %s %s -j -O %s" % (obabel_path, input_file1, input_file2, output_file)
    convert_result(cmd, output_file)


def extract_pdbqt(pdbqt_file, output_dir, index: int):
    """
    提取多构象pdbqt文件中的某个或者全部
    :param pdbqt_file: 输入的多构象pdbqt文件
    :param output_dir: 输出文件夹
    :param index: 提取第几个。如果为0则提取全部。
    :return 输出的文件列表
    """
    output_files = []
    if index == 0:
        first_lines, last_lines = read_models(pdbqt_file)
        with open(pdbqt_file) as f:
            i = 0
            while i < len(first_lines):
                f.seek(0)
                output_pdbqt = output_dir + os.sep + pdbqt_file.split(".")[0].split(os.sep)[-1] + "_" \
                               + str(i + 1) + ".pdbqt"
                model = f.readlines()[first_lines[i]:last_lines[i] + 1]
                with open(output_pdbqt, "w") as writer:
                    writer.writelines(model)
                output_files.append(output_pdbqt)
                i += 1
        return output_files

    else:
        first_lines, last_lines = read_models(pdbqt_file)

        # 如果选择构象大于实际构象
        try:
            first_line = first_lines[index - 1]
            last_line = last_lines[index - 1] + 1
            max_num = index
        except IndexError:
            first_line = first_lines[-1]
            last_line = last_lines[-1] + 1
            max_num = str(len(first_lines))

        with open(pdbqt_file) as f:
            splited_molecule = f.readlines()[first_line:last_line]
            output_pdbqt = output_dir + os.sep + pdbqt_file.split(".")[0].split(os.sep)[-1] + "_" + str(
                max_num) + ".pdbqt"
            with open(output_pdbqt, "w") as writer:
                writer.writelines(splited_molecule)
            output_files.append(output_pdbqt)
        return output_files


def read_models(pdbqt_file):
    with open(pdbqt_file) as f:
        first_lines = []
        last_lines = []
        for (line_num, line_value) in enumerate(f):
            if line_value.startswith("MODEL"):
                first_lines.append(line_num)
            if line_value == "ENDMDL\n":
                last_lines.append(line_num)
    return first_lines, last_lines


def convert_result(cmd, output_file):
    """
    执行命令，并查看是否成功
    :param cmd: 命令
    :param output_file:输出文件
    :return 是否转换成功
    """
    exit_code = os.system(cmd)
    if exit_code == 0:
        print("------------------------------------------------------------")
        print("%s转换成功" % output_file)
        print("------------------------------------------------------------")
        return True
    else:
        print("------------------------------------------------------------")
        print("%s准备失败，可能文件内部格式有误" % output_file)
        print("------------------------------------------------------------")
        return False
