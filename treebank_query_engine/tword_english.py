
import sqlite3
import re
import sys
import os
import glob
conn = sqlite3.connect('Treebank_English.db')
print ('Opened database successfully');

i=0
path="/home/guruprasad/Desktop/Intern_IIITH/treebanks/UD_English-EWT/*.conllu"

files = sorted(glob.glob(path))  # for open files of a folder
for name in files:  # for open files in a sequence
    with open(name) as f:
        	for line in f:
                    if '# sent_id' in line:
                        a=re.split(r'= ',line)
                        sid=a[-1].rstrip()
                    elif re.match("^\d+",line):
                        Case1 = "NULL"
                        Gender1 = "NULL"
                        Number1 = "NULL"
                        Person1 = "NULL"
                        PronType = "NULL"
                        VerbForm="NULL"
                        Voice= "NULL"
                        Mood = "NULL"
                        Tense = "NULL"
                        NumType = "NULL"
                        Poss = "NULL"
                        Foreign1= "NULL"
                        Definite= "NULL"
                        Degree= "NULL"
                        Reflex= "NULL"
                        Typo= "NULL"
                        Abbr= "NULL"
                        parent="NULL"
                        rel = "NULL"
                        SpaceAfter = "NULL"
                        CopyOf= "NULL"
                        CheckReln= "NULL"
                        CheckAttachment= "NULL"
                        CheckUPOS = "NULL"
                        res=re.findall(r'\S+',line)
                        word=res[1]
                        root=res[2]
                        pos_UD=res[3]
                        pos_ILMT=res[4]
                        wid=res[0]
                        parent=res[6]
                        rel=res[7]
                        i=i+1
                        b = re.findall(r'[^\|]+', res[5])
                        for words in b:
                            if re.match('Case=', words):
                                Case1 = re.split(r'=', words)[-1]
                            elif re.match('Gender=', words):
                                Gender1 = re.split(r'=', words)[-1]
                            elif re.match('Number=', words):
                                Number1 = re.split(r'=', words)[-1]
                            elif re.match('Person=', words):
                                Person1= re.split(r'=', words)[-1]
                            elif re.match('PronType=', words):
                                PronType= re.split(r'=', words)[-1]
                            elif re.match('VerbForm=', words):
                                VerbForm = re.split(r'=', words)[-1]
                            elif re.match('Voice=', words):
                                Voice= re.split(r'=', words)[-1]
                            elif re.match('Mood=', words):
                                Mood= re.split(r'=', words)[-1]
                            elif re.match('Tense=', words):
                                Tense= re.split(r'=', words)[-1]
                            elif re.match('NumType=', words):
                                NumType= re.split(r'=', words)[-1]
                            elif re.match('Poss=', words):
                                Poss = re.split(r'=', words)[-1]
                            elif re.match('Foreign=', words):
                                Foreign1 = re.split(r'=', words)[-1]
                            elif re.match('Definite=', words):
                                Definite= re.split(r'=', words)[-1]
                            elif re.match('Degree=', words):
                                Degree = re.split(r'=', words)[-1]
                            elif re.match('Reflex=', words):
                                Reflex = re.split(r'=', words)[-1]
                            elif re.match('Typo=', words):
                                Typo= re.split(r'=', words)[-1]
                            elif re.match('Abbr=', words):
                                Abbr = re.split(r'=', words)[-1]
                        a = re.findall(r'[^\|]+', res[-1])
                        for words in b:
                            if re.match('SpaceAfter=', words):
                                SpaceAfter = re.split(r'=', words)[-1]
                            elif re.match('CopyOf=', words):
                                CopyOf= re.split(r'=', words)[-1]
                            elif re.match('CheckReln=', words):
                                CheckReln = re.split(r'=', words)[-1]
                            elif re.match('CheckAttachment=', words):
                                CheckAttachment= re.split(r'=', words)[-1]
                            elif re.match('CheckUPOS=', words):
                                CheckUPOS= re.split(r'=', words)[-1]

                        path1=re.split(r'/',name)
                        print(i,sid,word)
                        conn.execute('INSERT INTO Tword(SNo,sid,word,wid,root,pos_UD,pos_ILMT,Case1,Gender1,Number1,Person1,PronType,VerbForm,Voice,Mood,Tense,NumType,Poss,Foreign1,Definite,Degree,Reflex,Typo,Abbr,parent,rel,SpaceAfter,CopyOf,CheckReln,CheckAttachment,CheckUPOS,filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(i,sid,word,wid,root,pos_UD,pos_ILMT,Case1,Gender1,Number1,Person1,PronType,VerbForm,Voice,Mood,Tense,NumType,Poss,Foreign1,Definite,Degree,Reflex,Typo,Abbr,parent,rel,SpaceAfter,CopyOf,CheckReln,CheckAttachment,CheckUPOS,path1[-1]))
                        conn.commit()
                    else:
                        continue

conn.close()
f.close()
