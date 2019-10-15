#Function to extract dictionary from H_wordid-word_mapping.dat
def create_dict(filename,string):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip(string).strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)

def eng_root_word_from_morph(e_word):
   cmd='echo "'+e_word+'" | lt-proc -ac $HOME_anu_test/apertium/en.morf.bin | apertium-retxt'
   cmd1 = 'echo "work"'
   #print(cmd)
   output=subprocess.check_output(cmd, shell=True)
   final=output.decode("utf-8")
   #print(final)
   root=re.findall(r'\/(.*?)\<',final)
   if len(root)==0 :
      root.append(e_word) 
   if(len(set(root))==1):
      e_root_word=root[0]
   else:
      return -1
   #print(e_root_word)
   return e_root_word



def hin_root_word_from_morph(h_word):
   cmd='echo "'+h_word+'" | lt-proc -ac $HOME_anu_test/bin/hi.morf.bin | apertium-retxt'
   output=subprocess.check_output(cmd, shell=True)
   final=output.decode("utf-8")
   #print(final)
   root=re.findall(r'\/(.*?)\<',final)
   if len(root)==0 :
      root.append(h_word)
   #listChar = ['z','z','z','z']
 
   if(len(set(root))==1):
         h_root_word=root[0]
   else:
         return -1
   return h_root_word


def extract_dictionary_ordered_fact(filename):
    dict1={}
    with open(filename, "r") as f:
        data = f.read().split("\n")
        while "" in data:
            data.remove("")
        dict1={}
        #print(data)
        for entry in data:
            #print(entry)
            x = re.findall("(id-root \w+ \w+ )",entry)[0].split(" ")
            #x = re.findall("(id-root \w+ \w+ )",entry)[0].split("\t")
            #print(x)
            dict1[x[1]]=x[2]
        #print("\n",dict1)
    return(dict1)

def extract_dictionary_ordered_fact_H_root(filename):
    dict1={}
    with open(filename, "r") as f:
        data = f.read().split("\n")
        while "" in data:
            data.remove("")
        #print(data)
        for entry in data:
            #print(entry)
            x = re.findall("(H_headid-root\t\w+\t\w+)",entry)[0].split("\t")
            #str="(H_headid-root\t" + word_id +"\t"+entry.split("\t")[2]+")"
            #x = re.findall("(id-root \w+ \w+ )",entry)[0].split("\t")
            #print(x)
            dict1[x[1]]=x[2]
        #print("\n",dict1)
    return(dict1)


def extract_dictionary_ordered_fact_database_mng(filename):
    dict1={}
    with open(filename, "r") as f:
        data = f.read().split("\n")
        while "" in data:
            data.remove("")
        #print(data)
        for entry in data:
            #print(entry)
            #x = re.findall("(id-org_wrd-root-dbase_name-mng \w+ \w+ \w+ \w+ \w+)",entry)[0].split("\t")
            
            x = re.findall("(id-org_wrd-root-dbase_name-mng \w+ \w+ \w+ \w+)",entry)
            #y = re.findall("(.* \w+)",entry)
            dict_source = entry.split(" ")[4]
            hindi_equivalent = " ".join(entry.split(" ")[5:]).strip(")")
            #print(hindi_equivalent)
            if len(x)>0:
                key = x[0].split(" ")[3]
                val = hindi_equivalent
                #print(key,val)
                if  key in dict1:
                    dict1[key].append(val)
                else:
                    dict1[key]=[val]
  
        #print("\n",dict1)
    return(dict1)

#extract all words having E_word and E_root as same.(function works for hindi word and root too.)
def check_word_and_root_same(e2w, e_root_dict):
   id_word=[]
   for kw,vw in e2w.items():
       for kr,vr in e_root_dict.items():
           xx=[];yy=[] 
           if vw==vr:
               xx.append(kr)
               xx.append(vr)
           if len(xx)>0:
              id_word.append(xx)
   #print("\n",id_word)
   return(id_word)


#Function which checks exact match of Eng root == Eng word and Hindi root == Hindi word
def exact_match_WSD_modulo(einfo, hinfo, db):
   #print("=========================================")
   print(einfo)
   print(hinfo)
   print(db)
   e=[x[1] for x in einfo]
   h=[x[1] for x in hinfo]
   #print(list(db.keys()))
   #print(e)
   #print(h)
   exact_match=[]
   for eentry in e:
       for hentry in h:
           if eentry in list(db.keys()):
               for mng1 in db[eentry]:
                   if(mng1 == hentry):
                       pair=[eentry, hentry]
                       exact_match.append(pair)
   print(exact_match)
   return(exact_match)     

no_root=['kA','ke','kI','ko','se','ne','meM','Ora','yA', 'kyA', 'waraha', 'ki','kevala','lekina','jabaki','waWA','xVArA','nahIM','Pira','hI    ','BI']


def remove_duplicate_list(a):
   #b_set = set(map(tuple,a))  #need to convert the inner lists to tuples so they are hashable
   #b = map(list,b_set) #Now convert tuples back into lists (maybe unnecessary?)
   #----
   #b_set = set(tuple(x) for x in a)
   #b = [ list(x) for x in b_set ]
   #b.sort(key = lambda x: a.index(x) )
   #----
   b = list()
   for sublist in a:
       if sublist not in b:
           b.append(sublist)
   return b

import itertools
def remove_duplicate_lists_from_list_of_lists(k):
   return list(k for k,_ in itertools.groupby(k))

import os
def add(fact_items,string,filename):
    #print("inside writefact.add")
    #print(fact_items)
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename,"a") as f:
        for line in fact_items:
            tokens=len(fact_items)
            fact="("+string
            for i,a in enumerate(line):
                fact=fact+"\t"+str(a)
                #print(fact)
            fact=fact+")\n"
            #print(fact)
            f.write(fact)
            #print("File created")

#This function reads manju mam's database_meaning.dat and create database_mng_preprocessed.dat which add _ in hindi meanings having >1 words
def preprocess_database_mng(db,db1):
    with open(db) as f:
        all_entries = f.read().split("\n")
        with open(db1, 'w') as f1:
            for x in all_entries:
                if len(x.split(" "))>3:    #handled entries having more than 3 columns 
                    if x.split(" ")[4]=='default-iit-bombay-shabdanjali-dic_smt.gdbm':  #working on entries from only this dict
                        hind_meaning=x.split(" ")[5:]
                
                        if len(hind_meaning)>1:
                            hindi="_".join(hind_meaning)
                        else:
                            hindi=hind_meaning[0]
                        #print(" ".join(x.split(" ")[0:5])+" "+hindi)
                        f1.write(" ".join(x.split(" ")[0:5])+" "+hindi+"\n")
            
       

import sys, re
import pandas as pd
import numpy as np
from collections import OrderedDict 
import csv






def exact_match(tmp_dir):

	try:
	    root_tam_file = tmp_dir +'/verb_root_tam_info'
	    h_root_info_file = tmp_dir + '/H_headid-root_info_from_morph_and_parser.dat'
	    #bring hindi root for all nouns directly from H_headid-root_info_from_morph_and_parser.dat
	    #merge hindi root for verbs, from H_headid-root_info_from_morph_and_parser.dat and verb_root_tam_info
	    h_root_dict = extract_dictionary_ordered_fact_H_root(h_root_info_file)
	except:
	    print("File Missing: " + root_tam_file +'/' + h_root_info_file )

	try:
	    e_root_file = tmp_dir + '/revised_root.dat'   #get english root for N and verbs too
	    root_tam_grouping = tmp_dir + '/tam_id.dat' # to get english tam part of verb  (equivalent to root:.. of yukti)
	    root_tam_grouping_final = tmp_dir + '/E_lwg.dat' # to get english grouping of verb  (similar to VP_expr_by_hindi_parser[this is a group of hindi words], tam_id.dat is group of proper ids)
	    e_root_dict = extract_dictionary_ordered_fact(e_root_file)
	except:
	    print("Issue with files: " + e_root_file +'/'+root_tam_grouping +'/'+root_tam_grouping_final)

	try:
	    db = tmp_dir + '/database_mng.dat'
	    db1 = tmp_dir + '/database_mng_preprocessed.dat'
	    preprocess_database_mng(db,db1)
	    db_dict = extract_dictionary_ordered_fact_database_mng(db1)
	except: 
	    print("Issue with files: " + db)
	   
	try:
	    h_word_file = tmp_dir + '/H_wordid-word_mapping.dat'
	    h2w = create_dict(h_word_file, '(H_wordid-word')
	    #print("\n",h2w)
	except:
	   print("File Missing: " + h_word_file )

	try:
	   e_word_file = tmp_dir + '/E_wordid-word_mapping.dat'
	   e2w = create_dict(e_word_file, '(E_wordid-word')
	   #print("\n",e2w)
	except:
	   print("File Missing: " + e_word_file )

	try:
		e_word_root_same = check_word_and_root_same(e2w, e_root_dict)
		#print(e_word_root_same) 
		h_word_root_same = check_word_and_root_same(h2w, h_root_dict) 
		a = exact_match_WSD_modulo(e_word_root_same, h_word_root_same, db_dict)
		b = remove_duplicate_lists_from_list_of_lists(a)
		#print("\n",b)
		add(b, "exact_match_WSD_modulo" , tmp_dir + "/A_exact_match_WSD_modulo.dat" )
		return(b)
	except:
		print("FIle missing in module4 ")    

	print("=========================================")

tmp_dir = sys.argv[1]
#db = tmp_dir + '/database_mng.dat'
#db1 = tmp_dir + '/database_mng_preprocessed.dat'
#preprocess_database_mng(db,db1)

exact_match(tmp_dir)
