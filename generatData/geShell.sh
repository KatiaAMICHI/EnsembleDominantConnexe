#!/bin/bash

# prend en entré un linkstream et faire resortir tout les arrete sans le temps de définition et unique dans une fichier .linkstream.points

FILES=../res/gen_enron/decoData
for f in `ls $FILES`
do
  awk '{printf("%s\t%s\n", $3, ($2>$3)?$3:$2, ($2>$3)?$2:$3)}' $FILES/$f | sort | uniq > $FILES/$f.points
  echo "Processing $f file... : $FILES/$f  et $f.points"
done