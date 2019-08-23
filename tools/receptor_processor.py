from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import Structure, Model, Chain, Select
from Bio.PDB import PDBIO
from Bio import SeqIO
import lxml.etree as et
from urllib.request import urlopen


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
    def extract_chain(structure: Structure, chain_ids: list, output_path: str):

        output_file = output_path + "/preped.pdb"
        ChainExtractor.structure = structure

        if len(chain_ids) == 0:
            io = PDBIO()
            io.set_structure(structure)
            io.save(output_file)
            return

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
    # s = PDBParser().get_structure("3ln1", "D:/Desktop/3ln1.pdb")
    # extractor = LigandExtractor(s, 0, "A", "CEL")
    # extractor.extract_ligand("D:/Desktop")
    chain_ex = ChainExtractor("D:/Desktop/2az5.pdb", "D:/Desktop")
    judge = chain_ex.judge_homo()
    if judge:
        print(judge)
