import sqlite3
import sys
import glob
import re
conn = sqlite3.connect('/home/kailash/HDTB_Query_engine-master/Treebank_Hindi_test2.db')
print ('Opened database successfully');
path = '/home/kailash/treebanks/UD_Hindi-HDTB/hi_hdtb-ud-dev.conllu'#change folder name  or path here
i = 0
files = sorted(glob.glob(path))
for name in files:
	with open(name) as f:
		res2 = re.split(r'/', name)
		name1 = res2[-1]
		for line in f:
			if '# sent_id' in line:
				res = re.split(r'= ', line)
				sid = res[-1].rstrip()
			elif re.match(r'^\d+', line):
				i=i+1
				res = re.split(r'	', line)
				a = res[-1]
				res1 = re.split(r'[=\|]', a)
				n = len(res1)
				for j in range(n):
					if res1[j]=='Translit':
						Translit = res1[j+1].rstrip()
					if res1[j]=='ChunkType':
						chunktype = res1[j+1]
					if res1[j]=='ChunkId':
						chunkid = res1[j+1]
				n1 = len(res)
				for k in range(n1):
					res[k]=res[k].rstrip()
				print(i)
				conn.execute('INSERT INTO Tchunk(SNo,sid,wid,word,parent,rel,chunkid,chunktype,Translit,filename) VALUES(?,?,?,?,?,?,?,?,?,?)',(i, sid, res[0], res[1], res[6], res[7], chunkid, chunktype, Translit, name1))
				conn.commit()
	f.close()
conn.close()
