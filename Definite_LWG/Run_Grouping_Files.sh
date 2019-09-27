#!/bin/bash


python3 $HOME_alignment/Definite_LWG/E_Sanity_Check.py $1
python3 $HOME_alignment/Definite_LWG/E_Grouping_Word_Dependency_Sanity.py $1
python3 $HOME_alignment/Definite_LWG/H_Grouping_Word.py $1
