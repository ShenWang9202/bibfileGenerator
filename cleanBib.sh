#!/bin/bash
biber --tool --configfile=remabs.conf $1
fileName=$(echo $1 | cut -d"." -f1)
VAR1="_bibertool.bib"
VAR2="$fileName$VAR1"
echo "$VAR2"
python bibcure/bibcure.py -i "$VAR2" -o $2
