
#env requiremnets : conda activate python3.6
#This code has dependency of graphviz [and import libraries..]
# This code will create a tree named H(which_lang)_tree.png in the 2.1 folder.

from __future__ import print_function
from itertools import groupby
import tree
import os, pandas as pd
import AnuLibrary, writeFact, tree
from operator import itemgetter
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import sys,  writeFact, os

path = '/home/kishori/a/tmp_anu_dir/tmp/GeoE01_tmp/2.45/'
#which_lang = 'H_cc_'
#relation_df = AnuLibrary.create_dataframe(path + 'cc_resolved.dat')  


#which_lang = 'E_cc'
#relation_df = AnuLibrary.create_dataframe(path + 'cc_resolved_eng.dat')  

#which_lang = 'H'
#relation_df = AnuLibrary.create_dataframe(path + 'hindi_dep_parser_original.dat')  
which_lang = 'E'
relation_df = AnuLibrary.create_dataframe(path + 'E_conll_parse')  


relation_df
# n = df.shape[0]

cid_hid = writeFact.extractUnlabelledDependency(relation_df)
cid_hid
hid_cid = tree.reverse_tuple_list(cid_hid)
hid_cid
tree.draw_tree(relation_df, hid_cid, which_lang, path)
