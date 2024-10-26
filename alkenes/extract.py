#!/usr/bin/env python3

import numpy as np
import pandas as pd
import cclib

no_to_symbol = {
    1:  "H",
    6:  "C",
    17: "Cl",
    9:  "F"
}

symbol_to_no = {v: k for k, v in no_to_symbol.items()}

bases = ["6-31G", "6-31G(d)", "631G(d,p)", "cc-pvdz", "cc-pvtz"]
n_isomers = 6
n_bases = len(bases)
n_atoms = 10

energies = np.zeros((n_isomers, n_bases))
charges = np.empty((n_isomers, n_bases), dtype=object)
dipolar_moments = np.zeros((n_isomers, n_bases))
iso_names = [f"ISO{i}" for i in range(1, n_isomers + 1)]

atom_nos = np.zeros((n_isomers, n_bases, n_atoms))

def read_charges(data):
    atom_types = data.atomnos
    
    reading_charges = {}
    
    atoms_read = np.ones(120)
    for i, charge in enumerate(data.atomcharges["mulliken"]):
        atom = atom_types[i]
    
        index = no_to_symbol[atom] + str(atoms_read[atom].astype(int))
    
        reading_charges[index] = float(charge)
        atoms_read[atom] += 1

    return reading_charges


def parse_file(filename):
    res = {}
    with open(filename, "r") as f:
        for line in f:
            # SCF Done:  E(RHF) =  -712.538505674     A.U. after   14 cycles
            if 'SCF Done' in line:
                res["energy"] = line.split()[4]
            # Dipole moment (field-independent basis, Debye):
            # X= -1.6012  Y= 2.3970  Z= 0.0000  Tot= 2.8826
            if 'Dipole moment (field-independent basis, Debye):' in line:
                line = next(f)
                res["dipole"] = line.split()[7]
    return res


# for i_isomer in range(1, n_isomers+1):
#     for i_base in range (1, n_bases+1):
#         filename = f"output/ISO{i_isomer}-base{i_base}.gjf"
#         data = cclib.io.ccread(filename)
#         
#         charges[i_isomer][i_base] = read_charges(data)
#
#         parsed = parse_file(filename)
#
#         energies[i_isomer][i_base] = parsed["energy"]
#         dipolar_moments[i_isomer][i_base] = parsed["dipole"]


df = pd.DataFrame(energies, columns=bases, index=iso_names)

print(df)
# print(df.to_latex(index=False))

