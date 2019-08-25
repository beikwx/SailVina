import math
import os


class Box(object):

    def __init__(self, ligand):
        self.GY_BOX_RATIO = 0.23
        self.ligand = ligand

        self.center_x = None
        self.center_y = None
        self.center_z = None
        self.box_size = None

    def get_box(self):

        atoms_x = 0
        atoms_y = 0
        atoms_z = 0
        atoms = 0

        ligand_file = open(self.ligand)

        for line in ligand_file.readlines():
            if line.startswith("HETATM"):
                if line[13:14] != "H":
                    atoms_x += float(line[30:38])
                    atoms_y += float(line[38:46])
                    atoms_z += float(line[46:54])
                    atoms += 1

        self.center_x = round(atoms_x / atoms, 3)
        self.center_y = round(atoms_y / atoms, 3)
        self.center_z = round(atoms_z / atoms, 3)
        dis = 0

        # 放回指针
        ligand_file.seek(0, os.SEEK_SET)
        for line in ligand_file.readlines():
            if line.startswith("HETATM"):
                if line[13:14] != "H":
                    dis += (float(line[30:38]) - self.center_x) ** 2 + (float(line[38:46]) - self.center_y) ** 2 + \
                           (float(line[46:54]) - self.center_z) ** 2

        self.box_size = round(math.sqrt(dis / atoms) / self.GY_BOX_RATIO, 3)

        ligand_file.close()

        return self.center_x, self.center_y, self.center_z, self.box_size
