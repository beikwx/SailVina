import os
import urllib.request
from urllib.error import URLError, HTTPError
from xml.dom import minidom
import shutil

from tools.receptor_processor import prepare_receptor, gen_config
from tools.file_processor import mk_output_dir
from tools.format_convertor import three_d_2_pdb, pdb_mol2_2_pdbqt, \
    extract_pdbqt, ob_noh_xyz, pdbqt_2_pdb
from tools.dock_processor import vina_dock
from tools.read_scores import read_scores
from tools.rmsd import charnley_cal_rmsd

MAX_RMSD = 2.0


def validate_folder(target_folder):
    """
    用于验证一个文件夹中的pdb用vina对接是否可靠。
    :param target_folder: 验证的文件夹。里面包含需要的文件。
    比如选择D:\3lnk
    里面包含
    - 3lnk_ligand.sdf:共晶配体文件
    - 3lnk_pocket.pdb:位点文件。如果没有则对接整个蛋白
    - 3lnk_protein.pdb:蛋白文件
    :return:
    """
    if not os.path.isdir(target_folder):
        print("选择的必须是一个目录！")
        return

    # 创建处理目录
    process_folder = os.path.join(target_folder, "process")
    mk_output_dir(process_folder)

    # 获取其中的文件
    input_protein = None
    input_ligand = None
    input_pocket = None
    config_file = []

    # 获取pdbid，所选文件夹就是
    pdb_id = os.path.split(target_folder)[-1]
    if len(pdb_id) != 4:
        print("%s不是pdbid!" % pdb_id)
        return

    print("----------正在解析文件夹%s----------" % target_folder)

    files = os.listdir(target_folder)
    for file in files:
        if "protein" in file:
            input_protein = os.path.join(target_folder, file)
        if "ligand" in file:
            input_ligand = os.path.join(target_folder, file)
        if "pocket" in file:
            input_pocket = os.path.join(target_folder, file)
        if "config" in file:
            config_file.append(os.path.join(target_folder, file))

    if input_protein is None or input_ligand is None:
        print("%s缺少配体或者受体，无法验证！" % target_folder)
        return

    if input_pocket is None:
        print("%s缺少口袋文件，将搜索整个蛋白进行重对接" % target_folder)

    print("输入的配体是%s:" % input_protein)
    print("输入的受体是%s:" % input_ligand)
    print("输入的口袋是%s:" % input_pocket)

    print("----------准备从网络获取pdb信息----------")

    # 1.获取pdb信息

    # 1.1目标网址https://www.rcsb.org/pdb/rest/describePDB?structureId=xxxx
    website = "https://www.rcsb.org/pdb/rest/describePDB?structureId=%s" % pdb_id
    try:
        response = urllib.request.urlopen(website, timeout=10)
    except HTTPError as e:
        print("服务器无法处理请求！")
        print("错误代码: ", e.code)
        print("----------无法获取pdb信息------")
        pdb_title = pdb_id
        pdb_keywords = "not_found"
        print("该pdb的标题是:%s" % pdb_title)
        print("该pdb的关键词是:%s" % pdb_keywords)
    except URLError as e:
        print("无法连接到服务器!")
        print("原因: ", e.reason)
        print("----------无法获取pdb信息------")
        pdb_title = pdb_id
        pdb_keywords = "not_found"
        print("该pdb的标题是:%s" % pdb_title)
        print("该pdb的关键词是:%s" % pdb_keywords)
    else:
        xml_data = response.read().decode("utf-8")  # 1.2解析xml文件
        dom = minidom.parseString(xml_data)
        pdb_node = dom.documentElement.getElementsByTagName('PDB')[0]

        pdb_title = pdb_node.getAttribute("title")
        pdb_keywords = pdb_node.getAttribute("keywords")

        print("该pdb的标题是:%s" % pdb_title)
        print("该pdb的关键词是:%s" % pdb_keywords)

    # 2.进行对接

    # 2.1准备受体
    preped_protein = os.path.join(process_folder, "preped.pdbqt")
    if input_protein.endswith(".pdbqt"):
        print("----------发现准备过的受体----------")
        shutil.copy(input_protein, preped_protein)
    else:
        print("----------准备受体----------")
        result = prepare_receptor(input_protein, preped_protein, "None", 0, 1, 1, 1, 1)
        if not result:
            print("----------准备受体失败，受体可能存在问题，请修复后重新尝试----------")
            return

    # 2.2准备配体
    preped_ligand = os.path.join(process_folder, "ligand.pdbqt")
    pdb_ligand = None
    if input_ligand.endswith(".pdbqt"):
        print("----------发现准备过的配体----------")
        shutil.copy(input_ligand, preped_ligand)
    else:
        print("----------准备配体----------")
        pdb_ligand = os.path.join(process_folder, "ligand.pdb")
        three_d_2_pdb(input_ligand, pdb_ligand, 0, "")
        pdb_mol2_2_pdbqt(pdb_ligand, preped_ligand)

    # 2.3准备config文件
    if len(config_file) == 0:
        if input_pocket is None:
            print("----------准备config文件----------")
            gen_config(preped_protein, preped_ligand)
        else:
            print("----------检测到口袋，准备口袋------")
            preped_pocket = os.path.join(process_folder, "preped_pocket.pdbqt")
            prepare_receptor(input_pocket, preped_pocket, "None", 0, 1, 1, 1, 1)
            print("----------准备config文件----------")
            gen_config(preped_pocket, preped_ligand)
    else:
        print("----------检测到config文件----------")
        for f in config_file:
            file_name = os.path.split(f)[-1]
            target_config_file = os.path.join(process_folder, file_name)
            shutil.copy(f, target_config_file)

    # 2.4进行对接
    configs = os.listdir(process_folder)
    output_folder = os.path.join(target_folder, "Output")
    mk_output_dir(output_folder)
    for config in configs:
        if "config" in config:
            config_file = os.path.join(process_folder, config)
            dock_output_file = os.path.join(output_folder, pdb_id + "_" + str(config[:-4]) + ".pdbqt")
            vina_dock(preped_ligand, preped_protein, config_file, dock_output_file)

    # 3.输出结果文件

    extract_folder = os.path.join(target_folder, "Extract")
    mk_output_dir(extract_folder)

    dock_output_files = os.listdir(output_folder)
    for dock_output_file in dock_output_files:
        # 3.1切割对接结果文件
        pdbqt_file = os.path.join(output_folder, dock_output_file)
        extract_pdbqt(pdbqt_file, extract_folder, 0)

    # 3.2读取切割的每个文件的分数，同时计算RMSD
    xyz_folder = os.path.join(target_folder, "XYZ")
    mk_output_dir(xyz_folder)
    print("----------转换原始配体文件格式----------")
    xyz_ligand = os.path.join(xyz_folder, "ligand.xyz")
    if pdb_ligand is None:
        pdb_ligand = preped_ligand[:-2]
        pdbqt_2_pdb(preped_ligand, pdb_ligand)
    ob_noh_xyz(pdb_ligand, xyz_ligand)
    print("----------输出报告---------")
    report_file = os.path.join(target_folder, "report.txt")
    last_validate_folder = os.path.join(target_folder, "Validate")
    mk_output_dir(last_validate_folder)
    with open(report_file, "w") as f:
        f.writelines("Title:\t%s\n" % pdb_title)
        f.writelines("Keywords:\t%s\n" % pdb_keywords)
        f.writelines("Ligand_name\tscores\trmsd\n")
        for output_ligand in os.listdir(extract_folder):
            if output_ligand.endswith(".pdbqt"):
                ligand_name = output_ligand[:-6]
                sec_ligand = os.path.join(extract_folder, output_ligand)
                # 读取分数
                score = read_scores(sec_ligand)[0]
                # 转换格式
                sec_pdb_ligand = os.path.join(xyz_folder, ligand_name + ".pdb")
                sec_xyz_ligand = os.path.join(xyz_folder, ligand_name + ".xyz")
                pdbqt_2_pdb(sec_ligand, sec_pdb_ligand)
                ob_noh_xyz(sec_pdb_ligand, sec_xyz_ligand)
                # 删除中间体
                os.remove(sec_pdb_ligand)
                # 计算rmsd
                rmsd = charnley_cal_rmsd(xyz_ligand, sec_xyz_ligand, "none", "hungarian")
                # RMSD达到要求，复制文件到Validate目录
                if float(rmsd) <= MAX_RMSD:
                    dst = os.path.join(last_validate_folder, ligand_name + ".pdbqt")
                    shutil.copy(sec_ligand, dst)
                f.writelines("%s\t%s\t%s\n" % (ligand_name, score, rmsd))
    print("----------验证%s结束----------" % target_folder)


if __name__ == '__main__':
    validate_folder(r"D:\Desktop\1M17")
    # extract_pdbqt(r"D:\Desktop\3lnk\Output\3lnk_config1.pdbqt", r"D:\Desktop\3lnk\Extract", 0)
    # print(read_scores(r"D:\Desktop\1akv\Extract\1akv_config1_1.pdbqt")[0])
