import sqlite3
import sys
import glob
import re


conn = sqlite3.connect('/home/guruprasad/Desktop/Intern_IIITH/treebank _query_ engine/database final/Treebank_English.db')
print ('Opened database successfully');
cursor = conn.cursor()

i = 1

while i == 1:
    print("\tSelect an option to execute one of the following quries:\n\t1.No of words in a sentence\n\t2.No of minor field types and information\n\t3.POS combinations and respective records\n\t4.Identify parent(word) corresponding to each word in a given sentence\n\t5.To find the word and it's gender in a given sentence\n\t6.To obtain information about a given relation, including corresponding POS's and sentences\n\t7.To obtain sibling relations in a given sentence\n\t8.To obtain Noun followed by verb cases and print relation\n\t9.Quit \n\t Enter a number from 1-13 for queries and 14 to exit.")
    m = 0
    list0 = []
    list1 = []
    list2 = []
    choice = input("Enter your choice:")
    if choice == "1":
        sentenceid0 = input("Enter the sentence ID to obtain the corresponding number of words in the sentence")
        sentenceid = "'"+sentenceid0+"'"
        cursor.execute('Select count(word),sid from Tword where sid ='+sentenceid+'group by sid')
        rows = cursor.fetchall()
        leng = len(rows)
        for j in range(0,leng):
            print(rows[j][0]-1)
    elif choice == "2":
        f = open('morphdetails_english.txt','w')
        Options = input("Enter one of the following fields to view its types:Definite\nPronType\nNumber1\nMood\nPerson\nTense\nVerbForm\nNumType\nDegree\nCase1\nGender1\nPoss\nForeign1\nVoice\nReflex\nTypo\nAbbr\n")
        str1 = 'select ' +Options+',count(1) from Tword where '+Options+'!= "NULL" group by '+Options+';'
        cursor.execute(str1)
        rows = cursor.fetchall()
        leng = len(rows)
        print(1)
        for j in range(0,leng):
            print(rows[j])
        inp=input("Do you wish to view the word information of a specific type?(Y|N)?")
        if(inp=='Y' or inp=='y'):
            senttype = input("Enter the type of field you wish to view")
            senttype1 = "'"+senttype+"'"
            cursor1=conn.cursor()
            cursor1.execute('Select '+Options+',sid,filename,word from Tword where '+Options+'=='+senttype1)
            rows1 = cursor1.fetchall()
            leng1 = len(rows1)
            for j in range(0,leng1):
                f.write("sid:"+rows1[j][1]+"\tword:"+rows1[j][3]+"\tfilename:"+rows1[j][2]+"\n")
        f.close()


    elif choice == "3":
        str1='SELECT pos_UD,pos_ILMT,count(*) FROM Tword GROUP BY pos_UD, pos_ILMT ;'
        curr=conn.cursor()
        curr.execute(str1)
        abc=curr.fetchall()
        n=len(abc)
        #a=np.zeros(n)

        for i in range(0,n):
            print("pos_UD:" + abc[i][0] + '\t' +"pos_ILMT:" + abc[i][1] +'\t'+ "No. of occurrences:" + str(abc[i][2]) + '\n')
        choice1=input("Do you want to view all the occurrences of a certain type of pos_UD?\n Press(Y/N):")
        if(choice1=='Y' or choice1=='y'):
            str2='SELECT word,pos_UD,pos_ILMT FROM Tword;'
            pos_UD_type=input("Input the type of pos_UD :")
            pos_ILMT_type=input("Input the type of pos_ILMT:")
            curr.execute(str2)
            abc1=curr.fetchall()
            #print(abc1)
            n=len(abc1)
            f=open("UD-ILMT_occurrence_english.txt","w")
            for j in range(0,n):
                if pos_UD_type==abc1[j][1] and pos_ILMT_type==abc1[j][2]:
                    f.write("pos_UD:" + abc1[j][1] +"\t pos_ILMT:" + abc1[j][2] + " \t word:" +abc1[j][0] +"\n")
        f.close()

    elif choice == "4":
        sentenceid = input("Enter the sentence ID to word-parent-rel pairs")
        cursor.execute('Select a.sid,a.word, b.word, a.rel from Tword a,Tword b where a.parent = b.wid and a.sid = b.sid')
        rows = cursor.fetchall()
        leng = len(rows)
        f=open("word-parent_english.txt","w")
        for j in range(0,leng):
            if sentenceid in rows[j]:
                f.write(str(rows[j][1:4]))
                f.write("\n")
        f.close()
    elif choice == "5":
        sentenceid0 = input("Enter the sentence ID to obtain gender information")
        sentenceid = "'"+sentenceid0+"'"
        cursor.execute('select sid,word,gender1 from Tword where gender1 != "NULL" and sid ='+sentenceid)
        rows = cursor.fetchall()
        leng = len(rows)
        f=open("Word-Gender_english.txt","w")
        for j in range(0,leng):
            f.write(rows[j][1]+"-"+rows[j][2])
            f.write("\n")
        f.close()

    elif choice == "6":
        pick=input('Enter relation: ')
        pick1="'"+pick+"'"
        str1='SELECT p.pos_UD, c.pos_UD, count(1) FROM Tword p INNER JOIN Tword c ON p.wid = c.parent AND p.sid = c.sid WHERE c.rel='+pick1+' GROUP BY p.pos_UD, c.pos_UD;'
        curr=conn.cursor()
        curr.execute(str1)
        myresult = curr.fetchall()
        n = len(myresult)
        for i in range(n):
            print('p_pos: '+myresult[i][0]+'\tc_pos: '+myresult[i][1]+'\tn_occurances: '+str(myresult[i][2]))
        pick=input('Do u want to check cases(y/n): ')
        if pick=='y':
            pick=input('Enter pos of parent: ')
            pick2=input('Enter pos of child: ')
            pick3="'"+pick+"'"
            pick4="'"+pick2+"'"
            str1='SELECT p.word, c.word, p.sid, p.filename FROM Tword p INNER JOIN Tword c ON p.wid = c.parent AND p.sid = c.sid WHERE c.rel='+pick1+'AND p.pos_UD='+pick3+' AND c.pos_UD='+pick4+';'
            curr.execute(str1)
            myresult = curr.fetchall()
            n = len(myresult)
            f = open('relation_to_word_mapping_english.txt', 'w')
            for i in range(n):
                f.write('filename: '+myresult[i][3]+'\tsentence_id: '+myresult[i][2]+'\tp_word: '+myresult[i][0]+'\tc_word: '+myresult[i][1]+'\n')
            f.close()
    elif choice == "7":
        cursor.execute('Select distinct rel from Tword')
        rows = cursor.fetchall()
        leng = len(rows)
        print("The relation list in the corpus is:")
        for j in range(0,leng):
            print(rows[j][0])
        rel1_0 = input("Enter sibling relationship 1")
        rel2_0 = input("Enter sibling relationship 2")
        rel1 = "'"+rel1_0+"'"
        rel2 = "'"+rel2_0+"'"
        cursor1=conn.cursor()
        cursor1.execute('select distinct a.sid,b.parent from Tword a, Tword b where a.parent = b.parent  and a.sid = b.sid  and a.rel ='+rel1+' and b.rel ='+rel2)
        rows = cursor1.fetchall()
        for i in range(0,len(rows)):
            print(rows[i])

    elif choice == "8":
        f = open('noun-verb_english.txt','w')
        str1="SELECT t.word,t.pos_UD,t.rel,c.sentence,t.wid,c.sid FROM Tword t INNER JOIN Tsentence c ON t.sid=c.sid ;"
        cursor.execute(str1)
        abc=cursor.fetchall()
        n=len(abc)
        for i in range(n):
            if abc[i][1]=='NOUN' and abc[i+1][1]=='VERB' :
                f.write("Sentence:"+ abc[i][3]+"  Sentence ID:"+ abc[i][5] +"\nNOUN ID:"+str(abc[i][4])+" Word:"+abc[i][0]+"\tVERB ID:"+str(abc[i+1][4])+" Word:"+abc[i+1][0] +"\trelation:"+abc[i][2]+"\n")
        f.close()

    elif choice =='9':
        print("Please press N or n to exit the query engine\n")
    ip = input("Do you want to continue(y/n)?")
    if ip=="Y" or ip=='y':
        i = 1
    else:
        i = 0
