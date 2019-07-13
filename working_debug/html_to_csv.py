from bs4 import BeautifulSoup
import csv,sys,os
import pandas as pd

tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no
print("===========>",sent_no)


def parser2wordid(filename):
    with open(filename,"r") as f1:
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip('(H_parserid-wordid').strip(')').split("\t")
            p2w[t[1].lstrip("P")] = t[2]
    return(p2w)
    
filename =path_tmp +  '/H_parserid-wordid_mapping.dat'
p2w = parser2wordid(filename)
print(p2w)

html = open(path_tmp +'/'+ eng_file_name +'_table1.html').read()
soup = BeautifulSoup(html, "lxml")
table = soup.find('table')
table_rows = table.find_all('tr')
print(type(table))


l=[]
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)
df = pd.DataFrame(l)
#df1= df[9:-1]
#df2 = df1.drop(df1.columns[[-1]], axis=1)
#df2.to_csv(path_tmp +sent_no +'/'+ eng_file_name + "_"+sent_no + ".csv", index=False)
final = df[9:-1].drop(df.columns[[-1]], axis=1)
final=final[0:23]
final.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + ".csv", index=False)
print(final.shape)

print(final)
#print(final.iloc[1,4])
#print(type(final.iloc[1,4]))
#thing = final.iloc[1,4]
#x = thing.split("+")
#print(x)


def func(x):
	#print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	#print(type(x))
	#print(x)
	#print(x.tolist())
    	col = x.tolist()
    	new_col=[];all_series=[];final_cell_value=""
    	#listofcolumns=[]
    	if unicode('   anu_exact_match  ') in col:	
		#print("do nothing")
		new_col =[str(i) for i in col]
    	else:
		#print("START=> ",len(col),[ str(i) for i in col])
		for count, i in enumerate(col,0):
			if(i!= ' .'):
				#print(i.lstrip().rstrip())
				change = i.lstrip().rstrip()
				if '/' in change:
					#print("//////////////")
					possibilities = [str(i.lstrip().rstrip()) for i in change.split("/")]
					#print(possibilities)
					new2=[]
					for poss in possibilities:
						if '+' in poss:
							g = poss.split('+')
							#print(g)
							new1=[]
							for one in g:
								#print(one, "==>", p2w[one])
								new1.append(p2w[one])	
							final_cell_value1 = " ".join(new1)
							#print(final_cell_value1)
							new2.append(final_cell_value1)
						else:
							#print(poss,"==>", p2w[poss])
							final_cell_value2 = p2w[str(poss)]
		                                	#print(final_cell_value2)
							new2.append(final_cell_value2)
					final_cell_value = "/".join(new2)
					#print(final_cell_value)
					new_col.append(final_cell_value)
					
				elif '+' in change:
					#print("+++++++++++++")
					grouping = [str(i.lstrip().rstrip()) for i in change.split("+")]
					#print(grouping)
					new=[]
					for g in grouping:
						#print(g, "++>", p2w[g])
						new.append(p2w[g])	
					final_cell_value = " ".join(new)
					#print(final_cell_value)
					new_col.append(final_cell_value)
				else:
					#print("--------------")
					#print(str(change), "-->", p2w[str(change)])
					final_cell_value = p2w[str(change)]
					#print(final_cell_value)
					new_col.append(final_cell_value)
			
			else:
				final_cell_value = '0'
				new_col.append(final_cell_value)
				#print("dot")
    		#print("************************************************")
    	new_col.append(final_cell_value)
    	new_col = new_col[:-1]
    	#print("END  => ", len(new_col),new_col)
	new_x = pd.Series(new_col)
    	return(new_x)


new = final.apply(func)
print("----------------------------------------")
print(new)
print(type(new))
new.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv", index=False)


#print(new.iloc[0,0])
#col_names = new.columns.tolist()
#print(type(col_names))
#for i in col_names:
#	print(i, type(i))
#new_names=[]
#new=new[[new_names]]
#print(new)





dfs = pd.read_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv")
# dfs = pd.read_csv('BUgol2.1E_2.94.csv')
# display(dfs)

# print(dfs)
# print(dfs1)
# print(dfs)


# dfT = dfs.T

# print(dfT)
# dfT.index


# dfT.to_dict('index')
# dfT.to_html('test.html')
# print(dfT)

newdict = dfs.to_dict()
# print(newdict)
# print(newdict)
# info = new_dict[0]
# print(info)
# newdict1 = {k:v for k,v in newdict.items() if v !=' 0' }
newdict1={}; info={}
for key,vdict in newdict.items():
    if key == '0':
        info=vdict
    if key == '0':
        del(newdict[key])
        
for key,vdict in newdict.items():
    for k,v in vdict.items():
        if v == '0' or v == 0 :
            del (vdict[k])
    
    newdict1[key]=vdict
    
for k,v in newdict1.items():
    print(k,v)
# print(newdict)

print(info)

print("=======")
word_dict={}
for key,vdict in newdict1.items():
    for k,v in vdict.items():
#         print("(Alldebugfacts (A "+ str(key) +") (" + str(info[k].lstrip().rstrip()) + " " +str(v).lstrip().rstrip()+"))" )
        new_word_value =  "(" + str(info[k].lstrip().rstrip()) + " " +str(v).lstrip().rstrip() +")"
        if key in word_dict:
            word_dict[key].append(new_word_value)
        else:
            word_dict[key]=[new_word_value]
            
with open(path_tmp +'/'+ "Alldebug.dat","w") as f:
    
    for k,v in word_dict.items():
#     print(k,v)
        print("(Alldebugfacts (A "+ str(k) +") " + " ".join(v)+")" )
        f.write("(Alldebugfacts (A "+ str(k) +") " + " ".join(v)+")\n")



