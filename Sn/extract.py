#!/usr/bin/env python3

import periodictable
import numpy as np
import pandas as pd
import cclib


bases = ["lanl2dz", "sdd", "mp2", "sddmp2"]
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
    
        index = periodictable.elements[atom].symbol + str(atoms_read[atom].astype(int))
    
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


for i_isomer in range(n_isomers):
    for i_base in range (n_bases):
        filename = f"output/{i_isomer+1}-{bases[i_base]}.LOG"
        data = cclib.io.ccread(filename)
        
        charges[i_isomer][i_base] = read_charges(data)

        parsed = parse_file(filename)

        energies[i_isomer][i_base] = parsed["energy"]
        dipolar_moments[i_isomer][i_base] = parsed["dipole"]


# Dipolar moments
dipoles = pd.DataFrame(dipolar_moments, columns=bases, index=iso_names)
pd.options.display.float_format = "{:,.2f}".format
print("Dipolar moments (Debye)")
print(dipoles)
# print(dipoles.to_latex(index=False))
print()

# Energies
energies = pd.DataFrame(energies, columns=bases, index=iso_names)

pd.options.display.float_format = "{:,.7f}".format
print("Energies (Hartree)")
print(energies)
# print(energies.to_latex(index=False))
print()

# Delta energies
energies_kcal = energies * 627.503
min_energies_per_isomer = energies_kcal.min(axis=0)
delta_energies = energies_kcal.sub(min_energies_per_isomer, axis=1)

pd.options.display.float_format = "{:,.5f}".format
print("Delta energies (kcal/mol)")
print(delta_energies)

# Charges
# column_order = ["C1", "C2", "Sn1", "Sn2", "Br1", "F1", "H1", "H2", "H3", "H4"]
column_order = ["C1", "C2", "Sn1", "Sn2", "Br1", "F1"]
for i_isomer in range(n_isomers):
    df = pd.DataFrame.from_records(charges[i_isomer])
    df = df[column_order]
    df.index = bases
    print(df)
