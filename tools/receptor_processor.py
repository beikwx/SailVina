import math
import os
import sys

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import Structure, Model, Chain, Select
from Bio.PDB import PDBIO
from Bio import SeqIO
import lxml.etree as et
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from tools.check import Check
from tools.configer import Configer
from tools.file_path import prepare_receptor4_path
from tools.file_processor import gen_config_file, pdbqt2dir


def check_pdb_status(pdb_id):
    """
    从pdb中得到当前pdbid的情况，是否过时
    :returns 状态和当前id的小写
    """
    url = 'http://www.rcsb.org/pdb/rest/idStatus?structureId=%s' % pdb_id
    xml = None
    try:
        xml_file = urlopen(url, timeout=10)
    except HTTPError as e:
        print("服务器无法处理请求！")
        print("错误代码: ", e.code)
        xml = None
    except URLError as e:
        print("无法连接到服务器!")
        print("原因: ", e.reason)
        xml = None
    else:
        xml = et.parse(xml_file)
        xml_file.close()
    status = None
    current_pdb_id = pdb_id
    if xml is None:
        return ["UNKNOWN", current_pdb_id.lower()]
    for df in xml.xpath('//record'):
        # 查看状态，有'UNKNOWN', 'OBSOLETE', or 'CURRENT'
        status = df.attrib['status']
        # pdb_id过时，替换为新的
        if status == 'OBSOLETE':
            current_pdb_id = df.attrib['replacedBy']
    return [status, current_pdb_id.lower()]


def prepare_receptor(receptor: str, output_file: str,
                     fix_method: str, preserve_charges: int,
                     nphs: int, lps: int, waters: int, nonstdres: int):
    """
    使用ADT的prepareReceptor4准备受体。
    :param receptor: 受体路径。比如D:/test/a.pdb
    :param output_file: 输出路径。比如D:/test
    :param fix_method: 修复方法。"bonds_hydrogens", "bonds", "hydrogens", "checkhydrogens", "None"
    :param preserve_charges: 保留电荷。1或者0
    :param nphs:合并非极性氢。1或者0
    :param lps:合并电荷。1或者0
    :param waters:去水。1或者0
    :param nonstdres:去除非标准氨基酸。1或者0
    :return 准备成功返回真，失败返回假
    """
    u_para_list = []
    if nphs:
        u_para_list.append("nphs")
    if lps:
        u_para_list.append("lps")
    if waters:
        u_para_list.append("waters")
    if nonstdres:
        u_para_list.append("nonstdres")

    u_paras = ""
    for u_para in u_para_list:
        if u_para == u_para_list[-1]:
            u_paras += u_para
            break
        u_paras += u_para + "_"

    # print(u_paras)

    if preserve_charges:
        # 保留电荷,做处理
        if u_paras != "":
            cmd = "%s %s -r %s -o %s -A %s -C -U %s -e" % (Configer.get_para("python_path"), prepare_receptor4_path,
                                                           receptor, output_file,
                                                           fix_method, u_paras)
        # 保留电荷，不做处理
        else:
            cmd = "%s %s -r %s -o %s -A %s -C -e" % (Configer.get_para("python_path"), prepare_receptor4_path,
                                                     receptor, output_file,
                                                     fix_method)
    else:
        # 不保留电荷,做处理
        if u_paras != "":
            cmd = "%s %s -r %s -o %s -A %s -U %s -e" % (Configer.get_para("python_path"), prepare_receptor4_path,
                                                        receptor, output_file,
                                                        fix_method, u_paras)
        # 不保留电荷，不处理
        else:
            cmd = "%s %s -r %s -o %s -A %s -e" % (Configer.get_para("python_path"), prepare_receptor4_path,
                                                  receptor, output_file,
                                                  fix_method)
    exit_code = os.system(cmd)
    if exit_code == 0:
        print("------------------------------------------------------------")
        print("%s准备成功" % receptor)
        print("------------------------------------------------------------")
        return True
    else:
        print("------------------------------------------------------------")
        print("%s准备失败，请尝试使用biopython进行修复。" % receptor)
        print("------------------------------------------------------------")
        return False


def get_receptors(receptors_root_path):
    """
    返回一个目录下面的所有受体，只支持pdb格式
    :param receptors_root_path:
    :return: 所有受体的名称列表
    """
    receptors = os.listdir(receptors_root_path)
    receptors_name = []
    for receptor_path in receptors:
        if receptor_path.endswith(".pdb"):
            receptors_name.append(os.path.split(receptor_path)[-1])
    return receptors_name


def proteins2dir(proteins_dir):
    """
    将指定受体文件夹中的受体移动到以受体命名的文件夹中，将受体重命名为"preped.pdbqt"
    :param proteins_dir: 包含pdbqt受体的目录
    :return:生成的受体目录
    """
    receptors = __get_proteins(proteins_dir)
    if len(receptors) == 0:
        print("没有监测到受体文件！")
        return
    receptors_dir = []
    for receptor in receptors:
        pdbqt_path = proteins_dir + os.sep + receptor
        receptors_dir.append(os.path.splitext(pdbqt_path)[0])
        pdbqt2dir(pdbqt_path)
    return receptors_dir


def gen_config(protein, ligand):
    """
    在受体路径中创建多个config文件
    :param protein: 蛋白路径，比如r"./Proteins/pdb1/preped.pdbqt"
    :param ligand: 配体路径，比如r"./Ligands/aspirin.pdbqt"
    """
    x_cos, y_cos, z_cos, size = __gen_config_boxes(protein, ligand)
    count = 1
    for x in x_cos:
        for y in y_cos:
            for z in z_cos:
                filename = os.path.split(protein)[0] + os.sep + "config" + str(count) + ".txt"
                # print(filename)
                gen_config_file(filename, x, y, z, size)
                count += 1


def __gen_config_boxes(protein, ligand):
    """
    根据受体和配体生成多个config的盒子
    :param protein: 蛋白路径
    :param ligand: 配体路径
    :returns:x,y,z方向的所有坐标，盒子的大小
    """
    # 获取受体的盒子
    protein_box = __get_pdb_box(protein)
    # 获取配体的盒子
    ligand_box = __get_pdb_box(ligand)

    # 定义对接最大的盒子
    config_box_size = 30.0

    # print(protein_box)
    # print(ligand_box)

    # x方向需要的盒子
    x_count = math.ceil((protein_box[3] + ligand_box[3]) / (config_box_size - ligand_box[3]))
    y_count = math.ceil((protein_box[4] + ligand_box[4]) / (config_box_size - ligand_box[3]))
    z_count = math.ceil((protein_box[5] + ligand_box[5]) / (config_box_size - ligand_box[3]))
    # print(x_count, y_count, z_count)

    x_coordinates = []
    y_coordinates = []
    z_coordinates = []

    # 求config盒子的X坐标合集
    i = 0
    max_x = (protein_box[0] + 0.5 * protein_box[3] + ligand_box[3]) - 0.5 * config_box_size
    while i < x_count:
        x = (protein_box[0] - 0.5 * protein_box[3] - ligand_box[3]) + 0.5 * config_box_size + (
                config_box_size - ligand_box[3]) * i
        if x <= max_x:
            x_coordinates.append(round(x, 2))
        else:
            x_coordinates.append(round(max_x, 2))
        i += 1

    # 求config盒子的Y坐标合集
    i = 0
    min_y = (protein_box[1] - 0.5 * protein_box[4] - ligand_box[4]) + 0.5 * config_box_size
    while i < y_count:
        y = (protein_box[1] + 0.5 * protein_box[4] + ligand_box[4]) - 0.5 * config_box_size - (
                config_box_size - ligand_box[4]) * i
        if y >= min_y:
            y_coordinates.append(round(y, 2))
        else:
            y_coordinates.append(round(min_y, 2))
        i += 1

    # 求config盒子的Z坐标合集
    i = 0
    min_z = (protein_box[2] - 0.5 * protein_box[5] - ligand_box[5]) + 0.5 * config_box_size
    while i < z_count:
        z = (protein_box[2] + 0.5 * protein_box[5] + ligand_box[5]) - 0.5 * config_box_size - (
                config_box_size - ligand_box[5]) * i
        if z >= min_z:
            z_coordinates.append(round(z, 2))
        else:
            z_coordinates.append(round(min_z, 2))
        i += 1

    # print(x_coordinates)
    # print(y_coordinates)
    # print(z_coordinates)
    return x_coordinates, y_coordinates, z_coordinates, config_box_size


def __get_proteins(proteins_dir):
    """

    :param proteins_dir: 受体目录，其中是pdbqt的受体文件
    :return: 所有pdbqt文件的文件名
    """
    proteins = os.listdir(proteins_dir)
    receptors = []
    for protein in proteins:
        if protein.endswith(".pdbqt"):
            receptors.append(protein)

    print("------------------------------------------------------------")
    print("发现受体pdbqt文件" + str(len(receptors)) + "个")
    print("开始移动文件")
    return receptors


def __get_pdb_box(pdb_file_path):
    """
    计算蛋白或者配体的空间中心坐标和最大立方体长宽高。
    :param pdb_file_path: pdb或者pdbqt文件路径名
    :return: 中心x坐标，中心y坐标，中心z坐标，长，宽，高。
    """
    # 保证文件存在
    if not Check.check_file(pdb_file_path):
        print(pdb_file_path + "不存在")
        sys.exit()

    atoms_x_list = []
    atoms_y_list = []
    atoms_z_list = []

    # 额外距离
    extra_distance = 0

    # 读取所有非H原子的坐标
    with open(pdb_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                if line[13:14] != "H":
                    atoms_x_list.append(float(line[30:38]))
                    atoms_y_list.append(float(line[38:46]))
                    atoms_z_list.append(float(line[46:54]))

    if len(atoms_x_list) == 0:
        print("没有检测到原子")
        sys.exit()

    box_center_x = round(sum(atoms_x_list) / len(atoms_x_list), 3)
    box_center_y = round(sum(atoms_y_list) / len(atoms_y_list), 3)
    box_center_z = round(sum(atoms_z_list) / len(atoms_z_list), 3)

    box_length = round(max(atoms_x_list) - min(atoms_x_list), 1) + extra_distance
    box_width = round(max(atoms_y_list) - min(atoms_y_list), 1) + extra_distance
    box_height = round(max(atoms_z_list) - min(atoms_z_list), 1) + extra_distance

    return box_center_x, box_center_y, box_center_z, box_length, box_width, box_height


class ReceptorProcessor(object):

    @staticmethod
    def get_structure(pdb_path: str):
        parse = PDBParser(PERMISSIVE=1)
        pdb_id = pdb_path.split(os.sep)[-1].split(".")[0]
        structure = parse.get_structure(pdb_id, pdb_path)
        return structure

    @staticmethod
    def get_model_ids(structure: Structure):
        models = structure.get_models()
        model_list = []
        for model in models:
            model_list.append(model.get_id())
        return model_list

    @staticmethod
    def get_chain_ids(model: Model):
        chains = model.get_chains()
        chain_list = []
        for chain in chains:
            chain_list.append(chain.get_id())
        return chain_list

    @staticmethod
    def get_het_ids(chain: Chain):
        residues = chain.get_residues()
        residue_list = []
        for residue in residues:
            residue_id = residue.get_id()
            het_field = residue_id[0]
            het_name = residue.get_resname()
            if het_field != " " and het_field != "W":
                residue_list.append(het_name)
        return residue_list

    @staticmethod
    def get_het_id(hetname, chain: Chain):
        residues = chain.get_residues()
        for residue in residues:
            residue_id = residue.get_id()
            hetfield = residue_id[0]
            if hetfield != " " and hetfield != "W":
                if residue_id[0] == hetname:
                    return residue_id
        else:
            return None


class LigandExtractor(object):
    structure = None
    model_num = None
    chain_name = None
    residue_name = None

    model = None
    chain = None
    ligand = None

    def __init__(self, structure, model_num, chain_name, residue_name):
        LigandExtractor.structure = structure
        LigandExtractor.model_num = model_num
        LigandExtractor.chain_name = chain_name
        LigandExtractor.residue_name = residue_name

    def extract_ligand(self, save_path):
        # 拿到model对象
        LigandExtractor.model = LigandExtractor.structure[LigandExtractor.model_num]
        # 拿到chain对象
        LigandExtractor.chain = LigandExtractor.model[LigandExtractor.chain_name]
        # 拿到配体对象
        for protein_res in self.chain.child_list:
            if LigandExtractor.residue_name == protein_res.resname:
                LigandExtractor.ligand = protein_res

        class LigandSelect(Select):

            def accept_model(self, model):
                if model == LigandExtractor.model:
                    return 1
                else:
                    return 0

            def accept_chain(self, chain):
                if chain == LigandExtractor.chain:
                    return 1
                else:
                    return 0

            def accept_residue(self, residue):
                if residue == LigandExtractor.ligand:
                    return 1
                else:
                    return 0

        io = PDBIO()
        io.set_structure(self.structure)
        io.save(save_path + os.sep + "%s_%s.pdb" % (LigandExtractor.chain_name, LigandExtractor.residue_name), LigandSelect())


class ChainExtractor(object):
    structure = None
    chains = None

    @staticmethod
    def judge_homo(structure: str):
        message = []
        with open(structure, "rU") as handle:
            last_seq = None
            last_id = None
            seqs = SeqIO.parse(handle, "pdb-seqres")
            for record in seqs:
                seq = record.seq
                if seq == last_seq:
                    message.append(record.id.split(":")[-1] + "同源" + last_id)
                else:
                    last_seq = seq
                    last_id = record.id.split(":")[-1]
        if len(message) == 0:
            return False
        else:
            return message

    @staticmethod
    def extract_chain(structure: Structure, chain_ids: list, output_file: str):

        ChainExtractor.structure = structure

        # 如果为空则表示尝试修复后全部储存
        if len(chain_ids) == 0:
            io = PDBIO()
            io.set_structure(structure)
            io.save(output_file)
            return

        # 存储特定链的选择器
        class ChainSelect(Select):

            def accept_model(self, model):
                if model == ChainExtractor.structure[0]:
                    return 1
                else:
                    return 0

            def accept_chain(self, chain):
                chains = []
                for chain_id in chain_ids:
                    chains.append(ChainExtractor.structure[0][chain_id])
                if chain in chains:
                    return 1
                else:
                    return 0

        io = PDBIO()
        io.set_structure(structure)
        io.save(output_file, ChainSelect())


if __name__ == '__main__':
    pass
