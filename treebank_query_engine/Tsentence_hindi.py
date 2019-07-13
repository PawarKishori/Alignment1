import sqlite3
import sys
import glob
import re
conn = sqlite3.connect('/home/kailash/HDTB_Query_engine-master/Treebank_Hindi_test3.db')
print ('Opened database successfully');
path = '/home/kailash/treebanks/UD_Hindi-HDTB/hi_hdtb-ud-dev.conllu'#change folder name  or path here
i = 0
w = 0
files = sorted(glob.glob(path))
for name in files:
	with open(name) as f:
		res0 = re.split(r'/', name)
		name1 = res0[-1].rstrip()
		for line in f:
			if '# text' in line:
				res = re.split(r'= ', line)
				txt = res[-1].rstrip()
			elif '# sent_id' in line:
				res = re.split(r'= ', line)
				sid = res[-1].rstrip()
			elif re.match(r'^\d+', line):
				w=w+1
			elif line == '\n':
				i=i+1
				print(i)
				w=w-1
				conn.execute('INSERT INTO Tsentence(SNo,sid,sentence,words,filename) VALUES(?,?,?,?,?)',(i, sid, txt, w, name1))# for store data in a file and above lines are for reading a file according to my files data
				w=0 
				conn.commit()
				sent_id=""
				text=""
	f.close()
conn.close()
