#!bin/bash

for i in {1..6}; do
    cp "$1-sdd.chk" "$1-sddmp2.chk"
    echo ""

    echo '%mem=32GB' >> "$1-sddmp2.gjf"
    echo '%nproc=12' >> "$1-sddmp2.gjf"
    echo "%chk=$1-sddmp2.chk" >> "$1-sddmp2.gjf"
    echo '# opt freq=noraman mp2/sdd geom=allcheck' >> "$1-sddmp2.gjf"
    echo '' >> "$1-sddmp2.gjf"
    echo 'Title Card Required' >> "$1-sddmp2.gjf"
    echo '' >> "$1-sddmp2.gjf"

    G09 "$1-sddmp2"
done
