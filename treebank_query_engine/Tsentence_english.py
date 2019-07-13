import sqlite3
import re
import glob
conn = sqlite3.connect("Treebank_English_sentence.db")
print ('Opened database successfully');
i=0
w=0
path="/home/guruprasad/Desktop/Intern_IIITH/treebanks/UD_English-EWT/*.conllu"
files = sorted(glob.glob(path))  # for open files of a folder
for name in files:  # for open files in a sequence
	with open(name) as f:
		for line in f:

			if '# sent_id' in line:
				i=i+1
				a=re.split(r'= ',line)
				sid=a[-1].rstrip()
			elif re.match("^\d+",line):
				w+=1

			elif '# text' in line:
				res = re.split(r'= ',line)
				sentence=res[-1].rstrip()

			elif line=="\n":
				w-=1
				path1=re.split(r'/',name)
				print(i,sid)
				conn.execute('INSERT INTO Tsentence(Sno,sid,words,sentence,filename) VALUES(?,?,?,?,?)',(i,sid,w,sentence,path1[-1]))
				conn.commit()
				w=0


conn.close()
f.close()
