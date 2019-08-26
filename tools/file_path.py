import os

para_file = os.path.realpath(__file__) + os.sep + ".." + os.sep + ".." + os.sep + "para.txt"

pdbqt_to_pdb_path = os.path.realpath(__file__) + os.sep + ".." + os.sep + \
                    ".." + os.sep + "others" + os.sep + "pdbqt_to_pdb.py"

prepare_ligand4_path = os.path.realpath(__file__) + os.sep + ".." + os.sep + \
                       ".." + os.sep + "others" + os.sep + "prepare_ligand4.py"

prepare_receptor4_path = os.path.realpath(__file__) + os.sep + ".." + os.sep + \
                         ".." + os.sep + "others" + os.sep + "prepare_receptor4.py"

vina_path = os.path.realpath(__file__) + os.sep + ".." + os.sep + ".." + os.sep + \
            "others" + os.sep + "vina.exe"

if __name__ == '__main__':
    print(prepare_ligand4_path, pdbqt_to_pdb_path, prepare_receptor4_path)
