import pandas as pd
import glob
import os
import sys
import numpy as np
#from html import HTML
from flask import Flask, render_template_string, session, request
from bs4 import BeautifulSoup
from IPython.display import display, HTML
from sklearn.datasets import load_iris
from tkinter import *
import importlib.util
import csv

tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
path = tmp_path  + sys.argv[1] + '_tmp'
path1 = path+'/*/'
filename = sys.argv[1] + '.html'

out_path=os.getenv('HOME')+'/anu_output/'

#path = r'path1'                  # use your path
all_files = sorted(glob.glob(os.path.join(path1, "clips_to_csv_utf_words.csv")))
print(all_files)

root = Tk()

m = root.winfo_screenwidth()

html_string = '''
<html>
    <head></head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.css" rel="stylesheet"/>
    <link href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css" rel="stylesheet"/>

    <link rel="stylesheet" type="text/css" href="df_style.css" />
    <body>
    <script src = "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <div id="header">
    <input type="text" name="ser" id="ser" placeholder="Search..." />
    <div id="sent">
    </div>
    </div>  
    <script type="text/javascript", src = "myhtml.js"></script>
    <div id="dvCSV">
        <div id="mytable">
        	{table}
        </div>
    </div>
    </body>
</html>
    '''
table_list = []
measurer = np.vectorize(len)

for filename in all_files:
    if filename.endswith('.csv'):
        table_list.append(filename.split("/")[-1].split('.')[0]+'.'+filename.split("/")[-1].split('.')[1])        
lines = []
k=0  
df = []
print(table_list)


for f in all_files:
    pd.set_option("display.expand_frame_repr", True)
    df_from_each_file = pd.read_csv(f, sep="#", skiprows=3)
    
    
    pd.set_option("display.expand_frame_repr", True)
    line = pd.read_csv(f, sep="\n", nrows=2)
    df_from_each_file = df_from_each_file.replace(np.nan, '', regex=True)
    df_from_each_file.insert(0,'',table_list[k])
    k=k+1
    df_from_each_file.style.set_table_attributes('style="border-collapse:collapse"').set_table_styles([
        # Rest of styles
    ]).render()
    
    df.append(df_from_each_file)
    l = open('myhtml.txt', 'a')
    with open('myhtml.txt', 'a') as l:
        l.write(line.to_string()+"\n\n")
        l.close()
        
        
        
        
dfs = pd.concat(df, axis=1)
res1 = measurer(dfs.values.astype(str)).max(axis=0)
r = dfs.shape[0]
c = len(dfs.columns)

i=0
y=23
while (i < c):
    df1 = dfs.iloc[0:r, i:y]
    with open(out_path+sys.argv[1]+'.html', 'a') as f:
        f.write(html_string.format(table=df1.to_html(classes='mystyle')))
    i=y
    y=i+23
