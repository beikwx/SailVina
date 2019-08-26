import os


def vina_dock(ligand, protein, config, output):
    """
    使用vina命令进行对接
    :param ligand: 配体文件名 ./Ligands/ligand.pdbqt
    :param protein: 受体文件名 ./Proteins/pdb1/preped.pdbqt
    :param config: 配置文件名 ./Proteins/pdb1/config1.pdbqt
    :param output:输出文件名 ./Output/pdb1/01.pdbqt
    """

    cmd = "vina --ligand %s --receptor %s --config %s --out %s" % \
          (ligand, protein, config, output)

    # print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    pass
    # 本地调试代码
    # vina_dock(r".\Ligands\aspirin.pdbqt", r".\Proteins\01\preped.pdbqt", r".\Proteins\01\config1.txt",
    #           r".\Output\01\01.pdbqt")
