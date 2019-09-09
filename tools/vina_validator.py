import os
import urllib.request
from urllib.error import URLError, HTTPError
from xml.dom import minidom

from tools.receptor_processor import prepare_receptor, gen_config
from tools.file_processor import mk_output_dir
from tools.format_convertor import three_d_2_pdb, pdb_mol2_2_pdbqt, extract_pdbqt
from tools.dock_processor import vina_dock


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

    if input_protein is None or input_ligand is None:
        print("%s缺少配体或者受体，无法验证！" % target_folder)
        return

    if input_pocket is None:
        print("%s缺少口袋文件，将搜索整个蛋白进行重对接")

    print("输入的配体是%s:" % input_protein)
    print("输入的受体是%s:" % input_ligand)
    print("输入的口袋是%s:" % input_pocket)

    print("----------准备从网络获取pdb信息----------")

    # 1.获取pdb信息

    # 1.1目标网址https://www.rcsb.org/pdb/rest/describePDB?structureId=xxxx
    pdb_title = None
    pdb_keywords = None

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
    print("----------准备受体----------")
    preped_protein = os.path.join(process_folder, "preped.pdbqt")
    prepare_receptor(input_protein, preped_protein, "None", 0, 1, 1, 1, 1)

    # 2.2准备配体
    print("----------准备配体----------")
    pdb_ligand = os.path.join(process_folder, "ligand.pdb")
    three_d_2_pdb(input_ligand, pdb_ligand, 0, "")
    preped_ligand = os.path.join(process_folder, "ligand.pdbqt")
    pdb_mol2_2_pdbqt(pdb_ligand, preped_ligand)

    # 2.3准备config文件
    if input_pocket is None:
        print("----------准备config文件----------")
        gen_config(preped_protein, preped_ligand)
    else:
        print("----------检测到口袋，准备口袋------")
        preped_pocket = os.path.join(process_folder, "preped_pocket.pdbqt")
        prepare_receptor(input_pocket, preped_pocket, "None", 0, 1, 1, 1, 1)
        print("----------准备config文件----------")
        gen_config(preped_pocket, preped_ligand)

    # 2.4进行对接
    configs = os.listdir(process_folder)
    output_folder = os.path.join(target_folder, "Output")
    mk_output_dir(output_folder)
    for config in configs:
        if "config" in config:
            config_file = os.path.join(process_folder, config)
            dock_output_file = os.path.join(output_folder, pdb_id + "_" + config[:-4] + ".pdbqt")
            vina_dock(preped_ligand, preped_protein, config_file, dock_output_file)

    # 3.输出结果文件

    extract_folder = os.path.join(target_folder, "Extract")
    mk_output_dir(extract_folder)

    dock_output_files = os.listdir(output_folder)
    for dock_output_file in dock_output_files:
        # 3.1切割对接结果文件
        pdbqt_file = os.path.join(output_folder, dock_output_file)
        extract_pdbqt(pdbqt_file, extract_folder, 0)

    #


if __name__ == '__main__':
    validate_folder(r"D:\Desktop\3lnk")
    # extract_pdbqt(r"D:\Desktop\3lnk\Output\3lnk_config1.pdbqt", r"D:\Desktop\3lnk\Extract", 0)
