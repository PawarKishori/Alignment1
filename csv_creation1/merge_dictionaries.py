#!/usr/bin/env python
# coding: utf-8

# In[3]:

import sys

def merge(file1, file2):
    filenames = [file1, file2]
    with open(output_dict, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


input_dict = sys.argv[1]
input_dict1 = sys.argv[2]
output_dict = sys.argv[3]
# converting_dictionaries_into_list()
output_dict = merge(input_dict, input_dict1)

# merge("/home/user/anusaaraka/Anu_data/domain/multi_word_dic/tech_sample2","/home/user/anusaaraka/Anu_data/domain/tech_sample")


# In[ ]:
