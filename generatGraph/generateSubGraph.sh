#!/bin/bash

# Input : le chemin du fichier
#       FILES=../res/enron/enronCleanRename
#       FILES=../res/rollernet/rollernetCleanRename

max1=98277034
path1=../res/extractEnron/

max2=9976
path2=../res/extractRollernet/

i=0
c=982770
alph=0

while ((i < max2))
do
    echo "...................................................."

    # enron
    # alph=$(expr $i + 1900000)
    # awk '$1 >= int('$i') && $1<= int('$alph'){ print $2,$3 }' $1 | sort | uniq > $path1"extractEnron"$i".points"
    # i=$(expr $i + 1900000)

    # rollernet
    alph=$(expr $i + 200)
    awk '$1 >= int('$i') && $1<= int('$alph'){ print $2,$3 }' $1 | sort | uniq > $path2"extractRollernet"$i".points"
    i=$(expr $i + 200)

done
