import sys,re, os
k_en = sys.argv[1]
engG = sys.argv[2]
hinG = sys.argv[3]

tmp_path = '/'.join(k_en.split('/')[:-1])
#print(tmp_path)

k_grping_id =tmp_path + '/K_grouping_id.dat'
k_grping_id_corrected = tmp_path + '/K_grouping_id_corrected.dat'
k_id_word =tmp_path + '/K_id_word.dat'
k_enhanced_corrected = tmp_path + '/K_enhanced_corrected.dat'


#K_layer fact format file
with open (k_en, 'r') as f:
    data=f.read().split(",")
    k=data[1:]
#print(k)

k_id_word_dict = {}
for i,j in enumerate(k,1):
    k_id_word_dict[i]=j


with open(k_id_word, 'w') as f:
    for i,j in enumerate(k,1):
        #print(i,j)
        f.write("(K_id-word\t"+str(i)+'\t'+j.lstrip("((").rstrip("))")+ ')\n')


# Generation of K_grouping_id.dat from K_enhanced.dat
final=[]
grp = []
grp1 = []
flag = 0
f=0
for i,j in enumerate(k,1):
        
    if "((" in j:
        flag = 1
        grp.append((i,j))
    elif '((' not in j and '))' not in j and flag==1:
        grp.append((i,j))
    elif "))" in j and flag==1:
        grp.append((i,j))
        flag = 0
    
    elif flag == 0 and '((' not in j and '))' not in j :
        grp1=[]
        grp1.append((i,j))
     
    if grp1 not in final:
        final.append(grp1)
    if grp not in final:
        final.append(grp)

#print(final)
all_grouping = []
for x in final:
    if len(x) > 1:
        all_grouping = x
#print(all_grouping)

elem=[]
f = 0
final_grping = []
for i in all_grouping:
    if '((' in i[1]:
        f = 1
        elem.append(i)
    elif '((' not in i[1] and '))' not in i[1] and f == 1:
        elem.append(i)
    elif '))' in i[1] and f == 1:
        elem.append(i)
        f = 0
        #print(elem)
        final_grping.append(elem)
        elem = []
#print(final_grping)


#Final grouping information
ff_grp_k = [x for x in final if len(x)==1] + final_grping    

#print("\n")
#print(ff_grp_k)
#print("\n")

# Writting into K_grouping_id.dat
k_grps=[]
with open(k_grping_id,'w') as f:
    for i in ff_grp_k:
        #print(i)
        x = [str(k[0]) for k in i]
        #print(x)
        k_grps.append(x)
        f.write("(K_group_elements\t"+" ".join(x)+ ')\n')

#print(k_grps)


# Opening Saumya's grouping and storing into data
egrp = []
with open (engG, "r") as f:
    data=f.read().split("\n")
    while "" in data:
        data.remove("")
    for i in data:
        x = i.split('\t')[-1].strip(')').split(' ')
        #print(x)
        egrp.append(x)
#print(egrp)


def intersection_of_two_list(lst1, lst2): 
    common_element = [value for value in lst1 if value in lst2] 
    return common_element

def correcting_k_grouping(k_grps, egrp):
    to_check = [x for x in k_grps if len(x)>1]
    new_K_grp = [x for x in k_grps if len(x)==1]  #group with onle one elements

    #print(to_check)
    #print("\n")
    for grp in to_check:
        if grp not in egrp:   #Non matching groups of Saumya and K_group
            for eg in egrp: 
                xx = intersection_of_two_list(grp, eg)
                
                if len(xx)>0:
                    new = grp if len(grp) > len(eg) else eg 
                    #print(grp, eg, xx)
                    #print("=>", new)
                    
                    for l in new:             # removing only one elem-groups whenever it got merged into existing group
                        if [l] in new_K_grp:           
                            #print(l + ' already in new_K_grp')
                            new_K_grp.remove([l])
                    new_K_grp = new_K_grp + [new]

        if grp in egrp:
            new_K_grp = new_K_grp + [grp]

                
                  
       
    return(new_K_grp)

print("Saumya's grouping")
print(egrp)
print("K groupung")
print(k_grps)
    
new_K_grp = correcting_k_grouping(k_grps, egrp)   # Corrected K layer grouping, using Saumya's grouping

#print(new_K_grp)
#print("----------------------\n\n")

# Writing K_grouping_id_corrected.dat equivalent to K_grouping_id.dat in fact format
with open(k_grping_id_corrected,'w') as f:
    for i in new_K_grp:
        x = [k for k in i]
        f.write("(K_group_elements\t"+" ".join(x)+ ')\n')

# Writing K_enhanced_corrected.dat equivalent to K_enhanced.dat
#with open(k_enhanced_corrected, w) as f: 
#print(new_K_grp)

# Python code to sort the tuples using first element of sublist Inplace way to sort using sort() 
def Sort(sub_li): 
    sub_li.sort(key = lambda x: x[0]) 
    return sub_li 

def generate_K_enhanced_corrected(new_K_grp):
   x=[]
   for i in new_K_grp:
       temp = [int(k) for k in i]
       x.append(temp)
   print(x)
   y = Sort(x)
   print(y)
   print(k_id_word_dict)
   new_final_grp = []
   for i in y:
      #print(i, [k_id_word_dict[x].lstrip("((").rstrip("))") for x in i])
      n_grp = [k_id_word_dict[x].lstrip("((").rstrip("))") for x in i]
      if len(i)>1 :
          #print("(("+" ".join(n_grp)+"))")
          new_final_grp.append("(("+", ".join(n_grp)+"))")
      else:
          #print(n_grp[0])
          new_final_grp.append(n_grp[0])
   return(new_final_grp)
   
   
new_final_grp = generate_K_enhanced_corrected(new_K_grp)
new_final_grp.insert(0,"K_enhanced_corrected")
with open(k_enhanced_corrected, 'w') as f:
   f.write(", ".join(new_final_grp))
print("\nFinal grouping of K")
print(new_final_grp)
print("----------------------")
