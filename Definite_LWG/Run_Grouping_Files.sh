#!/bin/bash


python3 E_Sanity_Check.py $1
python3 E_Grouping_Word_Dependency_Sanity.py $1
python3 H_Grouping_Word.py $1