#!bin/bash

for i in {1..6}; do
    cp "$i-lanl2dz.chk" "$i-mp2.chk"
    echo ""

    echo '%mem=32GB' >> "$i-mp2.gjf"
    echo '%nproc=12' >> "$i-mp2.gjf"
    echo "%chk=$i-mp2.chk" >> "$i-mp2.gjf"
    echo '# opt freq=noraman mp2/lanl2dz geom=allcheck' >> "$i-mp2.gjf"
    echo '' >> "$i-mp2.gjf"
    echo 'Title Card Required' >> "$i-mp2.gjf"
    echo '' >> "$i-mp2.gjf"

    G09 "$i-mp2"
done 
