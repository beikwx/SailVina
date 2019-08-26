import os

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import Structure, Model, Chain, Select
from Bio.PDB import PDBIO
from Bio import SeqIO
import lxml.etree as et
from urllib.request import urlopen

from tools.configer import Configer
from tools.file_path import prepare_receptor4_path
from tools.check import Check


def check_pdb_status(pdb_id):
    """
    从pdb中得到当前pdbid的情况，是否过时
    :returns 状态和当前id的小写
    """
    url = 'http://www.rcsb.org/pdb/rest/idStatus?structureId=%s' % pdb_id
    xml_file = urlopen(url)
    xml = et.parse(xml_file)
    xml_file.close()
    status = None
    current_pdb_id = pdb_id
    for df in xml.xpath('//record'):
        # 查看状态，有'UNKWOWN', 'OBSOLETE', or 'CURRENT'
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
    else:
        print("------------------------------------------------------------")
        print("%s准备失败，请尝试使用biopython进行修复。" % receptor)
        print("------------------------------------------------------------")


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


class ReceptorProcessor(object):

    @staticmethod
    def get_structure(pdb_path: str):
        parse = PDBParser(PERMISSIVE=1)
        pdb_id = pdb_path.split("/")[-1].split(".")[0]
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
        io.save(save_path + "/%s_%s.pdb" % (LigandExtractor.chain_name, LigandExtractor.residue_name), LigandSelect())


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
