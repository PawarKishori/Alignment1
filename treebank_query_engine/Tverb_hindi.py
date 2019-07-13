import sqlite3
import sys
import glob
import re
conn = sqlite3.connect('/home/kailash/HDTB_Query_engine-master/Treebank_Hindi_train_verb.db')
print ('Opened database successfully');
path = '/home/kailash/treebanks/UD_Hindi-HDTB/hi_hdtb-ud-train.conllu'#change folder name  or path here
i = 0
files = sorted(glob.glob(path))
morph = ['Case', 'Gender', 'Number', 'Person', 'Aspect', 'VerbForm', 'Voice', 'Mood', 'Tense', 'Polite', 'Poss', 'Echo']
other = ['Vib', 'Tam', 'ChunkId', 'ChunkType', 'Translit', 'Stype', 'SpaceAfter', 'AltTag']
n = len(morph)
n1 = len(other)
for name in files:
	with open(name) as f:
		res0 = re.split(r'/', name)
		name1 = res0[-1].rstrip()
		for line in f:
			if '# sent_id' in line:
				res = re.split(r'= ', line)
				sid = res[-1].rstrip()
			elif re.match(r'^\d+', line) and 'VERB' in line:
				val = [None] * (n+n1)
				i=i+1
				res = re.split(r'\t', line)
				a = res[5]
				b = res[9]
				res1 = re.split(r'[=\|]',a)
				res2 = re.split(r'[=\|]',b)
				n2 = len(res1)
				n3 = len(res2)
				for j in range(n):
					flag = 0
					for k in range(n2):
						if k%2==0:
							if morph[j]==res1[k]:
								flag = 1
								val[j]=res1[k+1]
								break
					if flag==0:
						val[j] = 'NULL'
				for j in range(n1):
					flag = 0
					for k in range(n3):
						if k%2==0:
							if other[j]==res2[k]:
								flag = 1
								val[n+j]=res2[k+1]
								break
					if flag==0:
						val[n+j] = 'NULL'
				n2=len(val)
				for z in range(n2):
					val[z] = val[z].rstrip()
				print(i)
				conn.execute('INSERT INTO Tverb(SNo,sid,wid,word,Case_,Gender,Number_,Person,Aspect,VerbForm,Voice,Mood,Tense,Polite,Poss,Echo,Vib,Tam,ChunkId,ChunkType,Translit,Stype,SpaceAfter,AltTag,filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(i,sid,res[0],res[1],val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10],val[11],val[12],val[13],val[14],val[15],val[16],val[17],val[18],val[19],name1))
				conn.commit()
	f.close()
conn.close()
