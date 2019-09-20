#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %%HTML
# <style type="text/css">
# table.dataframe td, table.dataframe th {
#     border: 1px  black solid !important;
#   color: black !important;
# }
# </style>


# In[2]:


import os, sys
import anchor as a
import pandas as pd
import subprocess


#Specify path of sentence:
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# tmp_path='/home/kishori/a/tmp_anu_dir/tmp/BUgol_27_aug/'
# eng_file_name = 'cc_conjE'

# eng_file_name = 'E'
# sent_no = '2.14' #2.29, 2.21, 2.61, 2.14, 2.64

eng_file_name = sys.argv[1]
sent_no = sys.argv[2]

path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no
sent_dir =  tmp_path + eng_file_name + "_tmp/"
hfilename = path_tmp +  '/H_wordid-word_mapping.dat'
efilename = path_tmp + '/E_wordid-word_mapping.dat'
efilename_alternate = path_tmp + '/word.dat'

log_file = path_tmp + '/log_n1tohtml'

if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')
#---------------------------------------------------------------------------------

try:
    dfs = pd.read_csv(path_tmp +'/'+ "final_id.csv")
    del dfs['Unnamed: 0']
    no_of_eng_words = dfs.shape[1]
    title=list(dfs.columns.values)
    print(title)
except:
    print('final_id.csv missing')
    log.write("FILE MISSING: " + "final_id.csv"  + "\n")

#---------------------------------------------------------------------------------
try:   
    h2w = a.create_dict(hfilename, '(H_wordid-word')
    hdf=pd.DataFrame(list(h2w.values()), index=h2w.keys())

    show_hindi ={}    
    for k,v in h2w.items():
        show_hindi[k] = str(k)+"_"+v
    hin = [show_hindi[i] for i in sorted(show_hindi.keys())]
    hindi_word = list(show_hindi.values())
    hindi_row = "  ,  ".join(hindi_word)

except:
    print("FILE MISSING: " + hfilename )
    log.write("FILE MISSING: " + hfilename + "\n")
    


#------------------------------------------------------------------------------------

try:
    e2w = a.create_dict(efilename, '(E_wordid-word')
    edf=pd.DataFrame(list(e2w.values()), index=e2w.keys())
    show_eng ={}    
    for k,v in e2w.items():
        show_eng[k] = str(k)+"_"+v
    eng = [show_eng[i] for i in sorted(show_eng.keys())]
    title=["Resources"]+list(show_eng.values())
    print(title)
    
except:
    print("FILE MISSING: " + efilename )
    log.write("FILE MISSING: " + efilename+ "\n")
    command = "awk '{printf $3}' "+ efilename_alternate
    print(command)
    x=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True).stdout.read()
#     x1 = x.decode(encoding="utf-8", errors="strict")
    x1=x.decode("utf-8") 
    x2 = x1.split(")")
    while "" in x2:
        x2.remove("")
    print(x2, len(x2), type(x2))
    title=["Resources"] + list(x2[:-1])

#------------------------------------------------------------------------------------
#Prashant's and Apratim's module
try:
    prashant_csv = path_tmp + '/new_N1.csv'
    # print(open(prashant_csv,'r').read())
    N1_layer= a.load_row_from_csv(prashant_csv, 1)
    print(N1_layer)
    N1_layer.insert(0,"N1_layer")
    # print(N1_layer)
    print(N1_layer)
    
    dfs.loc[dfs.index[-1]+1] = N1_layer
    potential_anchor = a.extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Potential anchors (exact)')
    starting_anchor = a.extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Starting anchor')
    potential_anchor_partial = a.extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Potential anchors (partial)')
    potential_anchor_guess = a.extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Potential anchors (guess)')

    dfs
except:
    print("new_N1.csv not found")
    log.write("FILE MISSING: " + prashant_csv  + "\n")


# In[3]:


import re
#=====================================================
# try:
#     e_group_html = path_tmp + '/E_group_HTML.txt'
#     h_group_html = path_tmp + '/H_group_HTML.txt'

#     # Extracting and printing grouping information in [..][..] format
#     hindi_row_tooltip = "".join(a.load_row_from_csv(h_group_html, 0))
#     # print(hindi_row_tooltip)
#     hindi_row = "".join(a.load_row_from_csv(h_group_html, 1))
#     eng_row_tooltip = "".join(a.load_row_from_csv(e_group_html, 0))
#     eng_row = "".join(a.load_row_from_csv(e_group_html, 1))
# except:
#     print("E_group_HTML.txt not found")
#     log.write("FILE MISSING: " + "E_group_HTML.txt"  + "\n")



#Prashant's and Saumya's grouping information
try:
    egroup_file = path_tmp + '/E_Word_Group.txt'
    hgroup_file = path_tmp + '/H_Word_Group.txt'

    egroups = a.extract_from_grouping_ordered_facts(egroup_file)
    hgroups = a.extract_from_grouping_ordered_facts(hgroup_file)

    ecolor = ["MEDIUMBLUE","SKYBLUE","DARKGREEN","HOTPINK","SIENNA","SPRINGGREEN","REBECCAPURPLE","MOCCASIN","TEAL", "ORANGE","GREENYELLOW","KHAKI","AQUA","DARKGRAY","NAVY","ROSYBROWN","DARKSALMON","PAPAYAWHIP" ,"TAN", "THISTLE", "PALEVIOLETRED","LIGHTSALMON","LIGHTSTEELBLUE", "SANDYBROWN","ORCHID","CRIMSON", "OLIVE", "BLACK", "MEDIUMSPRINGGREEN","SALMON","PINK","SILVER", "CADETBLUE", "DARKKHAKI", "ROYALBLUE", "PERU" ,"TOMATO", "LAVENDER", "SEAGREEN","NAVAJOWHITE","PALEVIOLETRED","CORAL","CORNFLOWERBLUE","MAROON","SLATEGRAY","DODGERBLUE","PLUM","MEDIUMVIOLETRED","DARKSLATEGRAY", "MISTYROSE"]
    hcolor =["CRIMSON", "OLIVE", "BLACK", "MEDIUMSPRINGGREEN","SALMON","PINK","SILVER", "CADETBLUE", "DARKKHAKI", "ROYALBLUE", "PERU" ,"TOMATO", "LAVENDER", "SEAGREEN","NAVAJOWHITE","PALEVIOLETRED","CORAL","CORNFLOWERBLUE","MAROON","SLATEGRAY","DODGERBLUE","PLUM","MEDIUMVIOLETRED","DARKSLATEGRAY", "MISTYROSE","DARKMAGENTA","PURPLE","INDIGO","SLATEBLUE","LAWNGREEN","LIME","LIMEGREEN","PALEGREEN","LIGHTGREEN","MEDIUMSPRINGGREEN","FORESTGREEN","GREEN","OLIVEDRAB","DARKOLIVEGREEN","MEDIUMAQUAMARINE","DARKCYAN","CYAN","LIGHTCYAN","PALETURQUOISE","AQUAMARINE","DIMGRAY","LINEN","SNOW","HONEYDEW","SADDLEBROWN"]

    ecode = a.grouping_with_border_color_in_dataframe(egroups,"english", ecolor)
    hcode = a.grouping_with_border_color_in_dataframe(hgroups, "hindi",hcolor)
except:
    print("E_Word_Group.txt not found")
    log.write("FILE MISSING: " + 'E_Word_Group.txt'  + "\n")


try:
    start_dict ={}
    for i,val in enumerate(title,0):
        start_dict[i] = starting_anchor[i]
    print(start_dict)
    eng_hin_anchors=[]
    for item in range(1,no_of_eng_words):
        if start_dict[item]=='0':
            tmp=str(item) 
        else:
            tmp = str(item) + " ("+ str(start_dict[item])+")"
        eng_hin_anchors.append(tmp)
    print(eng_hin_anchors)


except:
    print("final_id.csv not found")
    log.write("FILE MISSING: " + 'final_id.csv'  + "\n")


#======================================================
#Bringing anchor information in english dataframe


try:
    edf_trans=edf
    edf_trans.insert(1,"new", eng_hin_anchors)
    edf_trans=edf_trans.set_index('new')
    edf_trans.index.name = None
    edf_trans.T
except:
    print("new exists hence wont insert again")

#======================================================
def id_to_word(x):
    show_hindi[0]='0'
#     print(show_hindi)
    col = x.tolist()
    new_col=[];all_series=[];final_cell_value=""

    if '   anu_exact_match  ' in col:
        new_col =[str(i) for i in col]
    else:
        for count, i in enumerate(col,0):
#             print(i, type(i))
            if i == '~':
                final_cell_value = '~'           #converted all int 0 to '0'
                new_col.append(final_cell_value)
                
            elif(i!= '0' and i!=0 ):  #code for those cell values which are neither '0' nor 0.
                i=str(i)           #changed all int to string
                change = i.lstrip().rstrip()
#                 print("===>", change) 
                pchange1 = change.replace('#', ' # ')
                pchange = pchange1.replace('/', ' / ')
#                 print(pchange)
                pchange_list = pchange.split()
#                 print(pchange_list)
                change1=[]
                for item in pchange_list:
                    if item=='#' :  #dont replace # and / with any word.
                        change1.append('#')
                    elif item =='/':
                        change1.append('/')
                    else:
                        if int(item) in show_hindi.keys():  # dict keys are int so typecasting item to int
                            change1.append(show_hindi[int(item)])  #here too typecasting needed
                    
#                 print(change1)
                final_cell_value=" ".join(change1)
                new_col.append(final_cell_value)
            
            
                
            else:
                final_cell_value = '0'           #converted all int 0 to '0'
                new_col.append(final_cell_value)
#         print("=======")        
            
    new_col.append(final_cell_value)
    new_col = new_col[:-1]
    new_x = pd.Series(new_col)
    return(new_x)


# In[4]:


# def id_to_IDSTR_on_string(i):
#     if (i=='Resources'):
#         return('Resources')
#     if(i!= '0' and i!=0):  #code for those cell values which are neither '0' nor 0.
#         i=str(i)           #changed all int to string
#         change = i.lstrip().rstrip()
# #                 print("===>", change) 
#         pchange1 = change.replace('#', ' # ')
    
#         pchange = pchange1.replace('/', ' / ')
# #                 print(pchange)
#         pchange_list = pchange.split()
# #                 print(pchange_list)
#         change1=[]
#         for item in pchange_list:
#             if item=='#' :  #dont replace # and / with any word.
#                 change1.append('#')
#             elif item =='/':
#                 change1.append('/')
#             else:
#                 if int(item) in show_hindi.keys():  # dict keys are int so typecasting item to int
#                     change1.append(show_hindi[int(item)])  #here too typecasting needed
                         
# #                 print(change1)
#         final_cell_value=" ".join(change1)
# #         new_col.append(final_cell_value)
                
#     else:
#         final_cell_value = '0'           #converted all int 0 to '0'
# #         new_col.append(final_cell_value)
#     return(final_cell_value)

# title = [id_to_IDSTR_on_string(i) for i in title]


import numpy as np
import H_Modules

new = dfs.apply(id_to_word)
print(title)
new.columns = title
new.index = np.arange(1,len(dfs)+1)
new=new.set_index('Resources')
# new.index.name="R"
new.index.name = None


es=open(path_tmp+ '/E_sentence').read()
hs=open(path_tmp + '/H_sentence').read()
hs = H_Modules.wx_utf_converter_sentence(hs)
himg = 'H_tree_final.png'
eimg = 'E_tree_final.png'

himg1 = 'H_tree_initial.png'
eimg1 = 'E_tree_initial.png'

himg2 = 'H_tree_corrected.png'
eimg2 = 'E_tree_corrected.png'





# In[5]:



# hindi_row="[1_This 2_range]    [3_consists]    [4_of 5_the 6_famous 7_valley]    [8_of 9_Kashmir]    [10_the 11_Kangra]    [12_and]    [13_Kullu 14_Valley]    [15_in 16_Himachal 17_Pradesh]    "
# hindi_row_tooltip="This range _ consists _ of the famous valley _ of Kashmir _ the Kangra _ and _ Kullu Valley _ in Himachal Pradesh"

def write_to_html_file(df, filename=''):
    '''
    Write an entire dataframe to an HTML file with nice formatting.
    '''

    result = '''
<html>
<head>
<style>
h3{
text-align: center;
}
h4{
text-align: center;
}




/* Style the tab */
.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}

/* Style the tab content */
.hcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}


/* -------- Tooltip ---------- */

.tooltip {
  position: relative;
  border-bottom: 1px dotted black;
  
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 1000px;
  background-color: black;
  color: #fff;
  
  border-radius: 6px;
  padding: 5px 0;
  
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  top: 100%;
  left: 50%;
  margin-left: -500px;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}

/* -------- /Tooltip ---------- */




.corner {
  width: 0;
  height: 0;
  border-top: 90px solid #ffcc00;
  border-bottom: 10px solid transparent;
  border-left: 90px solid transparent;
  position:fixed;
  right:0;
  margin:0px;
  z-index: 2;
}

.corner span {
  position:absolute;
  top: -80px;
  width: 100px;
  left: -106px;
  text-align: right;
  font-size: 20px;
  font-family: arial;
  font-weight: bold;
  display:block;
}




#gotoTop {
  display: none;
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 99;
  font-size: 18px;
  border: none;
  outline: none;
  background-color: #a5a5a5;
  color: white;
  cursor: pointer;
  padding: 12px;
  border-radius: 10px;
}

#gotoTop:hover {
  background-color: #555;
}




nav.float-action-button {
  position: fixed;
  bottom: 0;
  right: 0;
  margin: 90px 10px;
}

a.buttons {
  box-shadow: 0 5px 11px -2px rgba(0, 0, 0, 0.18), 0 4px 12px -7px rgba(0, 0, 0, 0.15);
  border-radius: 50%;
  width: 56px;
  height: 56px;
  color: #000;
  font-size: 18px;
  padding: 15px 0 0 0;
  text-align: center;
  display: block;
  margin: 20px auto 0;
  position: relative;
  -webkit-transition: all .1s ease-out;
  transition: all .1s ease-out;
}

a.buttons:active,
a.buttons:focus,
a.buttons:hover {
  box-shadow: 0 0 4px rgba(0, 0, 0, .14), 0 4px 8px rgba(0, 0, 0, .28);
  text-decoration: none;
}

a.buttons:not(:last-child) {
  width: 56px;
  height: 56px;
  margin: 20px auto 0;
  opacity: 0;
  font-size: 18px;
  padding-top: 15px;
  -webkit-transform: translateY(50px);
  -ms-transform: translateY(50px);
  transform: translateY(50px);
}

nav.float-action-button:hover a.buttons:not(:last-child) {
  opacity: 1;
  -webkit-transform: none;
  -ms-transform: none;
  transform: none;
  margin: 20px auto 0;
}

a.buttons:nth-last-child(1) {
  -webkit-transition-delay: 25ms;
  transition-delay: 25ms;
  background-color: #ffcc00;
  /* Button color */
}

a.buttons:nth-last-child(1) i.fa {
  transform: rotate3d(0, 0, 1, 0);
  transition: content 0.4s, transform 0.4s, opacity 0.4s;
}

a.buttons:nth-last-child(1):hover i.fa {
  transform: rotate3d(0, 0, 1, -180deg);
}

a.buttons:nth-last-child(1) i.fa:nth-last-child(1) {
  position: absolute;
  margin: 10px 0 0 -32px;
}

a.buttons:nth-last-child(1) i.fa:nth-last-child(2) {
  opacity: 0;
}

a.buttons:nth-last-child(1):hover i.fa:nth-last-child(1) {
  opacity: 0;
}

a.buttons:nth-last-child(1):hover i.fa:nth-last-child(2) {
  opacity: 1;
}

a.buttons:not(:last-child):nth-last-child(2) {
  -webkit-transition-delay: 50ms;
  transition-delay: 20ms;
  background-color: #ffcc00;
  /* Facebook color */
}

a.buttons:not(:last-child):nth-last-child(3) {
  -webkit-transition-delay: 75ms;
  transition-delay: 40ms;
  background-color: #ffcc00;
  /* Twitter color */
}

a.buttons:not(:last-child):nth-last-child(4) {
  -webkit-transition-delay: 100ms;
  transition-delay: 60ms;
  background-color: #ffcc00;
  /* Google plus color */
}

.tooltip.left {
  margin-left: -10px;
}



/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  position: relative;
  background-color: #fefefe;
  margin: auto;
  padding: 0;
  border: 1px solid #888;
  width: 80%;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
  -webkit-animation-name: animatetop;
  -webkit-animation-duration: 0.4s;
  animation-name: animatetop;
  animation-duration: 0.4s
}

/* Add Animation */
@-webkit-keyframes animatetop {
  from {top:-300px; opacity:0} 
  to {top:0; opacity:1}
}

@keyframes animatetop {
  from {top:-300px; opacity:0}
  to {top:0; opacity:1}
}

/* The Close Button */
.close {
    color: white;
    float: right;
    font-size: 35px;
    font-weight: bold;
	padding:15px;
}

.close:hover,
.close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
}

.modal-header {
  padding: 2px 16px;
  background-color: #5cb85c;
  color: white;
}

.modal-body {padding: 10px 16px;}

.modal-footer {
  padding: 2px 16px;
  background-color: #5cb85c;
  color: white;
}

/* English and Hindi DF's */

'''
    result += '{}' .format(ecode)
    result += '{}' .format(hcode)
   
    result += '''
    
</style>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
		<title>Anusaaraka Output</title>
		<link rel="stylesheet" type="text/css" href="../styles/css/normalize.css" />
		<link rel="stylesheet" type="text/css" href="../styles/css/demo.css" />
		<link rel="stylesheet" type="text/css" href="../styles/css/component.css" />
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
		<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery-throttle-debounce/1.1/jquery.ba-throttle-debounce.min.js"></script>
		<script src="../styles/js/jquery.stickyheader.js">
        <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
</script>
        
<script>
var sUsrAg = navigator.userAgent,
  usingChrome = sUsrAg.indexOf("Chrome") > -1;

if (!usingChrome) {
  alert("Please use Google chrome to access this page. Some features do not work in browsers other than Chrome.");
}
</script>       

</head>
<body>
    '''
    result += '<p class="corner"><span>%s</span></p>' % sent_no
    result += '<button onclick="topFunction()" id="gotoTop" title="Go to top">&#8679;</button>'
    result += '<br><h3> Sentence Number: %s &nbsp &nbsp &nbsp|&nbsp &nbsp &nbsp Reference English Text: <a href="iess102.pdf" target="_blank">English Chapter 2</a> &nbsp &nbsp &nbsp|&nbsp &nbsp &nbsp  Reference Hindi Text: <a href="ihss102.pdf" target="_blank">Hindi Chapter 2</a></h3><hr>' % sent_no
    result += '<h3> %s </h3>\n<hr>' % es
#     result += '<h3> %s </h3><button onclick="myFunction()">i</button>\n<hr>' % es
#     result += '<h4 class="tooltip"> {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(eng_row,eng_row_tooltip)

    result += '<h3> %s </h3>\n' % hs
#     result += '<h4 class="tooltip"> {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(hindi_row,hindi_row_tooltip)
#     result += '<span class="tooltiptext"> %s </span>\n' % hindi_row_tooltip
    result += df.to_html(classes='wide overflow-y', escape=False)
    #result += '<center> <img src="{0}"> <hr> <img src="{1}"> <hr> </center>' .format(eimg,himg)
#     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'

#     result += '<h4 class="tooltip"> English Grouping: {0} <span class="tooltiptext"> {1} </span></h4>\n <hr>' .format(eng_row,eng_row_tooltip)

#     result += '<h4 class="tooltip"> Hindi Grouping: {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(hindi_row,hindi_row_tooltip)

    result += '''
    
   
    
 <center><h2>English Dependency Parse Trees</h2></center>

<div class="tab">
  <button class="tablinks" onclick="openCity(event, 'E1')">English Final</button>
  <button class="tablinks" onclick="openCity(event, 'E2')">English Corrected</button>
  <button class="tablinks" onclick="openCity(event, 'E3')">English Initial</button>
</div>

<div id="E1" class="tabcontent">
  <h3>Transfored  Tree version2<br><br>Tree after local word grouping of intrachunk relations.</h3>
  '''
    result += '<center> <img src="{}"></center>' .format(eimg)
   
    result += '''
    
    
</div>

<div id="E2" class="tabcontent">
  <h3>Transfored  Tree version1<br><br>Changed obl tags and transformed cc-conj structure.</h3>
  '''
    result += '<center> <img src="{}"></center>' .format(eimg2)
    
    result += '''
    
</div>

<div id="E3" class="tabcontent">
  <h3>Original parse by parser<br><br>Stanford's 3.9 Dependency parse.</h3>
  '''
    result += '<center> <img src="{}"></center>' .format(eimg1)
    
    result += '''
</div>




 <center><h2>Hindi Dependency Parse Trees</h2></center>

<div class="tab">
  <button class="hlinks" onclick="hCity(event, 'H1')">Hindi Final</button>
  <button class="hlinks" onclick="hCity(event, 'H2')">Hindi Corrected</button>
  <button class="hlinks" onclick="hCity(event, 'H3')">Hindi Initial</button>
</div>

<div id="H1" class="hcontent">
  <h3>Transfored  Tree version2<br>Tree after local word grouping of intrachunk relations.</h3>
  '''
    result += '<center> <img src="{}"></center>' .format(himg)
   
    result += '''
    
</div>

<div id="H2" class="hcontent">
  <h3>Transfored  Tree version1<br><br>Changed obl tags and transformed cc-conj structure.</h3>

  '''
    result += '<center> <img src="{}"></center>' .format(himg2)
    
    result += '''
    
</div>

<div id="H3" class="hcontent">
  <h3>Orginal Parse<br><br>Irshad's Hindi Neural parse trained on UD annotated hindi treebank [IIIT].</h3>
  
    '''
    result += '<center> <img src="{}"></center>' .format(himg1)
    
    result += '''
</div>

    '''
#     result += '<center>{}></center>' .format(edf)
    try:
        result += edf_trans.T.to_html(classes="english", escape=False, index=False)
        result += hdf.T.to_html(classes="hindi", escape=False, index=False)
    except:
        print("edf try catch")
    
    '''
    
    '''
#     result += '<center style="padding-top:25px"><h4> Sentence Number: %s </h4></center>\n' % sent_no
#     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="800" height="700" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'

    result += '''
    <br>
<!-- dictionary links -->
<nav class="float-action-button"> 
        <a href="https://https://www.collinsdictionary.com/dictionary/english-hindi" target="_blank" class="buttons" title="Collins Dictionary" data-toggle="tooltip" data-placement="left">
          <i>Collin</i>
        </a>
       <a href="https://archive.org/details/in.ernet.dli.2015.464149" target="_blank" class="buttons" title="Collins Dictionary" data-toggle="tooltip" data-placement="left">
          <i>Kosh</i>
        </a>
		<a href="#" id="myBtn2" class="buttons" title="Sentence Observations" data-toggle="tooltip" data-placement="left">
          <i>Form</i>
        </a>
        <a href="#" class="buttons" title="Links" data-toggle="tooltip" data-placement="left">
          <i>Links</i>
   
        </a>
</nav>


<!-- The Modal -->
<div id="myModal2" class="modal">
<!-- Modal content -->
  <div class="modal-content">
      <span class="close second">&times;</span>
    <div class="modal-header">
      <h2>Form</h2>
    </div>
    <div class="modal-body">
      <p><center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center> </p>

    </div>
    <div class="modal-footer">
      <h3>Modal Footer</h3>
    </div>
  </div>
  </div>
</div>

<script>

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("gotoTop").style.display = "block";
    } else {
        document.getElementById("gotoTop").style.display = "none";
    }
   
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
 
     $('html, body').animate({scrollTop:0}, 'slow');
}

</script>

<script>
// Get the modal
var modal1 = document.getElementById("myModal1");
var modal2 = document.getElementById("myModal2");

// Get the button that opens the modal
var btn1 = document.getElementById("myBtn1");
var btn2 = document.getElementById("myBtn2");


// Get the <span> element that closes the modal
var span1 = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close second")[0];


// When the user clicks the button, open the modal
btn1.onclick = function() {
    modal1.style.display = "block";
}
btn2.onclick = function() {
    modal2.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span1.onclick = function() {
    modal1.style.display = "none";
}

span2.onclick = function() {
    modal2.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    }
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}
</script>

<script>
function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
</script>

<script>

function hCity(hevt, hName) {
  var j, hcontent, hlinks;
  hcontent = document.getElementsByClassName("hcontent");
  for (j = 0; j < hcontent.length; j++) {
    hcontent[j].style.display = "none";
  }
  hlinks = document.getElementsByClassName("hlinks");
  for (j = 0; j < hlinks.length; j++) {
    hlinks[j].className = hlinks[j].className.replace(" active", "");
  }
  document.getElementById(hName).style.display = "block";
  hevt.currentTarget.className += " active";
}
</script>

<script>
function myFunction() {
  var x = document.getElementById("myDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
</script>
</body>
</html>
'''
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(result)
#=======================================================================
write_to_html_file(new, path_tmp+'/final.html')
new.to_csv(path_tmp +'/final.csv')
# new.to_html(path_tmp +'/final.html')


# In[ ]:





# In[ ]:




