# coding: utf-8
#To run: python generate_root.py <path+hindi.morph.dat> <path+hindi_dep_parser_original.dat>

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


def POS_dep_to_morph_2_entries_handle(morph_pos, dep_pos, dep_pos_value):
   if dep_pos == dep_pos_value:
       if POS_Dict[dep_pos_value][0] == morph_pos:
           return 1
       elif POS_Dict[dep_pos_value][1] == morph_pos:
           return 1


def POS_check(morph_pos,dep_pos) :
    try :
        if dep_pos != "PUNCT":
            '''if dep_pos == "ADP":
                if POS_Dict["ADP"][0] == morph_pos :
                    return 1
                elif POS_Dict["ADP"][1] == morph_pos :
                    return 1'''
            if POS_dep_to_morph_2_entries_handle(morph_pos, dep_pos, "ADP"):
                return 1
            if POS_dep_to_morph_2_entries_handle(morph_pos, dep_pos, "ADV"):
                return 1
            else :
                if POS_Dict[dep_pos] == morph_pos :
                    return 1
        
        else :
            return 0
    except KeyError :
        ex="Key Error because of absence of morph POS of "+dep_pos
        if ex not in exception:
            exception.append(ex)
    
def Select_Root(filename,depname):
    log=[]
    head_root=[]
    with open(filename, "r") as f:
        data = f.read().split("\n")
        while "" in data:
            data.remove("")
    with open(depname, "r") as f:
        dep_data = f.read().split("\n")
        while "" in dep_data:
            dep_data.remove("")
    #with open(writeFile, 'w') as w:
    for entry in data:
        for dep in dep_data :
            if re.findall("H_word-root-cat-vib-case-gen-num-per-tam",entry) :
                #print(entry.split("\t")) #[3] is POS
                #print(entry.split("\t")[2]) #[3] is POS
                parser_id = dep.split("\t")[0]
                if entry.split("\t")[2] != '' :                     #'prsg' handled here
                    if entry.split("\t")[1]==dep.split("\t")[1]:
                        if POS_check(entry.split("\t")[3],dep.split("\t")[3]) :
                            word_id = p2w[int(parser_id)]
                            str="(H_headid-root\t" + word_id +"\t"+entry.split("\t")[2]+")"
                            if str not in head_root:
                                head_root.append(str)
                #elif entry.split("\t")[3] == 'prsg':
                #    if entry.split("\t")[1]==dep.split("\t")[1]:
                #        print(entry.split("\t")[1],dep.split("\t")[1])
                #        word_id = p2w[int(parser_id)]
                #        str="(H_headid-root\t"+ word_id +"\t" + entry.split("\t")[1]+")"
                #        if str not in head_root:
                #           head_root.append(str)
                elif entry.split("\t")[2] == '':
                    if entry.split("\t")[1]==dep.split("\t")[1]:
                        word_id = p2w[int(parser_id)]
                        str="(H_headid-root\t"+ word_id +"\t"+ entry.split("\t")[1]+")"
                        if str not in head_root:
                            head_root.append(str)  

                else :
                    str="Root for " +entry.split("\t")[1] + " doesn't exist"
                    print(str)
                    if str not in log:
                        log.append(str)
                        
    with open(path_tmp+"/H_headid-root_info_from_morph_and_parser.dat","w") as out:
        for i in head_root:
            print(i)
            out.write(i+"\n")
    with open(path_tmp+"/morph_and_parser_root_info_log","w") as err:
        for j in log:
            err.write(j+"\n")
    
        for i in exception :
            err.write(i+"\n")
    #writeFile = "H_headid-root_info.dat"




import re,sys
path_tmp = sys.argv[1]

#path_tmp="/".join(sys.argv[2].split("/")[:-1])
#out=open(path_tmp+"/H_headid-root_info_from_morph_and_parser.dat","w")
#err=open(path_tmp+"/morph_and_parser_root_info_log","w")

morphfile=sys.argv[1] + '/hindi.morph.dat'
depfile=sys.argv[1] + '/hindi_parser_canonial.dat'



exception=[]

POS_Dict={"PRON":"p","VERB":"v","ADP":("sh","prsg"),"NOUN":"n","ADJ":"adj","AUX":"v","DET":"v","PROPN":"n","SCONJ":"adj","ADV":("n","adj")}

#Added "ADV":("n","adj") in above list by the observations of:
'''
2.115/hindi_parser_canonial.dat:27	sarvAXika	_	ADV	_	_	28	advmod	_	_
2.25/hindi_parser_canonial.dat:2	bAhara	_	ADV	_	_	0	root	_	_
2.31/hindi_parser_canonial.dat:18	bahuwa	_	ADV	_	_	19	advmod	_	_
2.39/hindi_parser_canonial.dat:4	pahale	_	ADV	_	_	5	amod	_	_
2.42/hindi_parser_canonial.dat:2	ora	_	ADV	_	_	10	obl	_	_
2.49/hindi_parser_canonial.dat:1	Pira	_	ADV	_	_	4	advmod	_	_
2.60/hindi_parser_canonial.dat:3	pahale	_	ADV	_	_	10	obl	_	_
2.71/hindi_parser_canonial.dat:8	lagAwAra	_	ADV	_	_	9	advmod	_	_
2.75/hindi_parser_canonial.dat:9	jEse	_	ADV	_	_	14	obl	_	_
2.82/hindi_parser_canonial.dat:11	bahuwa	_	ADV	_	_	12	advmod	_	_
2.82/hindi_parser_canonial.dat:12	jalxI	_	ADV	_	_	14	advmod	_	_
2.8/hindi_parser_canonial.dat:12	uwwama	_	ADV	_	_	14	advmod	_	_
'''

no_root=['kA','ke','kI','ko','se','ne','meM','Ora','yA', 'kyA', 'waraha', 'ki','kevala','lekina','jabaki','waWA','xVArA','nahIM','Pira','hI','BI']


try:
    #hfilename = path_tmp +  '/H_wordid-word_mapping.dat'
    hparserid_to_wid = path_tmp + '/H_parserid-wordid_mapping.dat'
#try:   
#h2w = create_dict(hfilename, '(H_wordid-word')
    p2w = create_dict(hparserid_to_wid, '(H_parserid-wordid')
    print(p2w)
 
except:
    print("FILE MISSING: " + hparserid_to_wid )
#    log.write("FILE MISSING: " + hfilename + "\n")


Select_Root(morphfile,depfile)


#Write a function which will give correct root of VP in hindi using Yukti's output

