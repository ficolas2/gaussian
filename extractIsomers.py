#!/usr/bin/env python3

import periodictable
import numpy as np
import pandas as pd
import cclib
import sys


path_base = sys.argv[1]
if path_base[-1] == "/":
    path_base = path_base[:-1]

extract_path = path_base + "/extract"
path = path_base + "/output"
bases = []
bases_pretty = []
n_isomers = 0
atoms = []
distances_desc = []
with open(extract_path, "r") as f:
    bases = f.readline().strip().split(" ")
    bases_pretty = f.readline().strip().split(" ")
    n_isomers = int(f.readline().strip())
    atoms = f.readline().strip().split(" ")

    # From F-C(L), C-C(1-2/4-6) 
    # read [{atoms: ["F", "C"], type: "L"}, {atoms: ["C", "C"], type: "S", indices: [[1, 2], [4, 6]]}]
    distances = f.readline().replace(" ", "").strip().split(",")

    for distance in distances:
        desc_obj = {}
        desc_obj["atoms"] = distance.split("(")[0].split("-")
        description = distance.split("(")[1].replace(")", "")

        if "-" in description:
            desc_obj["type"] = "S"
            desc_obj["indices"] = []
            for indices in description.split("/"):
                indices_str = indices.split("-")
                desc_obj["indices"].append([int(indices_str[0]), int(indices_str[1])])

        else: 
            desc_obj["type"] = "L"

        distances_desc.append(desc_obj)


n_bases = len(bases)

energies = np.zeros((n_isomers, n_bases))
charges = np.empty((n_isomers, n_bases), dtype=object)
dipolar_moments = np.zeros((n_isomers, n_bases))
distances = np.zeros((n_isomers, n_bases, len(distances_desc)))
iso_names = [f"ISO{i}" for i in range(1, n_isomers + 1)]

def read_distances(data, distances):
    atom_types = data.atomnos
    coords = data.atomcoords[-1]

    for i, desc in enumerate(distances_desc):
        if desc["type"] == "L":
            atom1no = periodictable.elements.symbol(desc["atoms"][0]).number
            atom2no = periodictable.elements.symbol(desc["atoms"][1]).number
            distance_sum = 0
            count = 0
            for atom_index, atomno in enumerate(atom_types):
                if atom1no != atomno:
                    continue
                coord1 = coords[atom_index]
                min_distance = 10000
                for index2, coord2 in enumerate(coords):
                    if atom_types[index2] != atom2no:
                        continue
                    
                    calc_dist = np.linalg.norm(coord1 - coord2)
                    if calc_dist > 0.0001 and calc_dist < min_distance:
                        min_distance = calc_dist
                if atomno == 1 and min_distance > 1.3: # Botch because there are hydrogens that are bonded to Sn, and the distance between that and a carbon makes no sense to add to the average
                    continue
                distance_sum += min_distance
                count += 1
                
            distances[i] = distance_sum / count

                    
            
        elif desc["type"] == "S":
            mean_distance = 0
            for indices in desc["indices"]:
                mean_distance += np.linalg.norm(
                    coords[indices[0] - 1] - coords[indices[1] - 1]
                ) / len(desc["indices"])
            distances[i] = mean_distance



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
        filename = f"{path}/{i_isomer+1}-{bases[i_base]}.LOG"
        data = cclib.io.ccread(filename)
        
        charges[i_isomer][i_base] = read_charges(data)

        parsed = parse_file(filename)

        energies[i_isomer][i_base] = parsed["energy"]
        dipolar_moments[i_isomer][i_base] = parsed["dipole"]

        read_distances(data, distances[i_isomer][i_base])

# Distances
pd.options.display.float_format = "{:,.3f}".format
d = pd.DataFrame(distances[0])
print("Distanceas (Isomer 1) (Angstrom)")
# print(d)
print(d.to_latex(index=False, float_format="{:,.3f}".format))

d = pd.DataFrame(distances[2])
print("Distances (Isomer 3) (Angstrom)")
# print(d)
print(d.to_latex(index=False, float_format="{:,.3f}".format))

# Dipolar moments
# dipoles = pd.DataFrame(dipolar_moments, columns=bases_pretty, index=iso_names)
# pd.options.display.float_format = "{:,.3f}".format
# print("Dipolar moments (Debye)")
# print(dipoles)
# print(dipoles.to_latex(index=False))
# print()

# Energies
energies = pd.DataFrame(energies, columns=bases_pretty, index=iso_names)

pd.options.display.float_format = "{:,.7f}".format
print("Energies (Hartree)")
# print(energies)
print(energies.to_latex(index=False))
print()

# Delta energies (Hartree)
min_energies_per_isomer = energies.min(axis=0)
delta_energies = energies.sub(min_energies_per_isomer, axis=1)

# pd.options.display.float_format = "{:,.5f}".format
# print("Delta energies (Hartree)")
# print(delta_energies)
# print(delta_energies.to_latex(index=False))
# print()

# Delta energies
energies_kcal = energies * 627.503
min_energies_per_isomer = energies_kcal.min(axis=0)
delta_energies = energies_kcal.sub(min_energies_per_isomer, axis=1)

# pd.options.display.float_format = "{:,.5f}".format
# print("Delta energies (kcal/mol)")
# print(delta_energies)
# print(delta_energies.to_latex(index=False))
# print()

energies_kj = energies * 2625.5
min_energies_per_isomer = energies_kj.min(axis=0)
delta_energies = energies_kj.sub(min_energies_per_isomer, axis=1)

pd.options.display.float_format = "{:,.2f}".format
print("Delta energies (kJ/mol)")
# print(delta_energies)
print(delta_energies.to_latex(index=False, float_format="{:,.2f}".format))
# print()


print("Charges (Mulliken)")
pd.options.display.float_format = "{:,.3f}".format
# Charges
for i_isomer in range(n_isomers):
    df = pd.DataFrame.from_records(charges[i_isomer])
    df = df[atoms]
    df.index = bases_pretty
    print(df.to_latex(index=False, float_format="{:,.3f}".format))
    # print(df)
    # print()
