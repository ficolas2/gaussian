#!bin/bash

for i in {1..6}; do
    cp "$1-lanl2dz.chk" "$1-sdd.chk"
    echo ""

    echo '%mem=32GB' >> "$1-sdd.gjf"
    echo '%nproc=12' >> "$1-sdd.gjf"
    echo "%chk=$1-sdd.chk" >> "$1-sdd.gjf"
    echo '# opt freq=noraman hf/sdd geom=allcheck' >> "$1-sdd.gjf"
    echo '' >> "$1-sdd.gjf"
    echo 'Title Card Required' >> "$1-sdd.gjf"
    echo '' >> "$1-sdd.gjf"

    G09 "$1-sdd"
done
