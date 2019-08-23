import os
from tools.configer import Configer

pdbqt_to_pdb_path = os.path.realpath(
    __file__) + os.sep + ".." + os.sep + ".." + os.sep + "others" + os.sep + "pdbqt_to_pdb.py"
pdb_to_pdbqt_path = os.path.realpath(
    __file__) + os.sep + ".." + os.sep + ".." + os.sep + "others" + os.sep + "prepare_ligand4.py"
prepare_receptor4_path = os.path.realpath(
    __file__) + os.sep + ".." + os.sep + "others" + os.sep + ".." + os.sep + "prepare_receptor4.py"
python_path = Configer.get_para("python_path")

if __name__ == '__main__':
    print(pdb_to_pdbqt_path, pdbqt_to_pdb_path, prepare_receptor4_path)
