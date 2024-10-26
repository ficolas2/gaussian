#!/usr/bin/env python3

bases = ["6-31G", "6-31G(d)", "631G(d,p)", "cc-pvdz", "cc-pvtz"]

for i_isomer in range(1, 7):
    with open(f"ISO{i_isomer}.gjf", "r") as f:
        lines = f.readlines()
        for i_base, base in enumerate(bases):
            modified_lines = lines.copy()
            modified_lines[0] = f"%chk={i_isomer}-base{i_base+1}.chk\n"
            modified_lines[1] = f"# opt freq=noraman hf/{base} geom=connectivity\n"

            with open(f"output/{i_isomer}-base{i_base+1}.gjf", "w") as f_out:
                f_out.writelines(modified_lines)

