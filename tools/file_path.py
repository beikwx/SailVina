import os
import sys


para_file = os.path.realpath(sys.argv[0]) + os.sep + ".." + os.sep + "para.txt"
pdbqt_to_pdb_path = os.path.realpath(
    __file__) + os.sep + ".." + os.sep + ".." + os.sep + "others" + os.sep + "pdbqt_to_pdb.py"
pdb_to_pdbqt_path = os.path.realpath(
    __file__) + os.sep + ".." + os.sep + ".." + os.sep + "others" + os.sep + "prepare_ligand4.py"
prepare_receptor4_path = os.path.realpath(
    __file__) + os.sep + ".." + os.sep + ".." + os.sep + "others" + os.sep + "prepare_receptor4.py"

if __name__ == '__main__':
    print(pdb_to_pdbqt_path, pdbqt_to_pdb_path, prepare_receptor4_path)
