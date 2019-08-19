import glob
import os, sys, subprocess
"""
Created by  -   Saumya Navneet & Prashant Raj
Date        -   19/August/2019
Purpose     -   To generate local groups based on POS information to help in word alignment.
Input       -   Enter the path to 'tmp' folder to iterate on all the translated sentences to generate word grouping.
Output      -   Inside the folder for every translation, a file 'E_Word_Group.txt' will be created containing details of word group.
Files used  -   cat_consistency_check.dat, original_word.dat

For any queries you may drop a message at - saumyanavneet26@gmail.com or prashantraj012@gmail.com
"""

def english_group():

    #Taking the path of the BUgol tmp folder
    tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
    path = tmp_path + sys.argv[1] + '_tmp'
    all_sentences = path + "/E_Word_Group_All_Sentences.txt"
    path = path + '/2.*'
    sentences = sorted(glob.glob(path))
    output_path = open(all_sentences,"w")
    output_path.flush()

    for sentence in sentences:      #Change according to the number of sentences

        #Reading the POS information of individual sentences
        pos_path = str(sentence) + '/cat_consistency_check.dat'

        #Reading the original words of individual sentences
        word_path = str(sentence)+'/original_word.dat'
        outpath = str(sentence)+'/E_Word_Group.txt'
        outpathHTML = str(sentence)+'/E_group_HTML.txt'

        output_file = open(outpath, "w")
        outHTML = open(outpathHTML,'w')
        outHTML.flush()
        output_file.flush()

        # Reading the files as an input
        word_details = open(word_path).readlines()
        pos_details = open(pos_path).readlines()
        
        word_file = list()
        pos_file = list()

        for i in pos_details:
            if "id-cat_coarse " in i:
                i = i[:-2]
                value = i.split()
                value = value[1:]
                value[0] = int(value[0])
                pos_file.append(value[:])
        pos_file.sort()


        for i in word_details:
            if "id-original_word " in i:
                i = i[:-2]
                value = i.split()
                value = value[1:]
                value[0] = int(value[0])
                word_file.append(value[:])

        out_list = []  # To store the local word groups
        temp_list = []  # Used to generate local word groups

        # Grouping of words according to their POS and English grammar rules
        for i in range(0, len(pos_file)):
            current_list = pos_file[i]
            # Taking current pos for grouping of current word group
            current_pos = current_list[1]
            prev_pos = ""
            prev_list = []

            if i != 0:
                prev_list = pos_file[i-1]
                # Taking previous pos for grouping of current word group
                prev_pos = prev_list[1]

            if current_pos in ['preposition']:
                if prev_pos in ['determiner', 'wh-determiner', 'adjective', 'number', 'noun', 'PropN', 'verb', 'particle', 'infinitive_to', 'conjunction', 'pronoun', 'wh-pronoun', 'adverb', 'wh-adverb']:
                    out_list.append(temp_list)
                    temp_list = []
                    temp_list.append(current_list[0])
                else:
                    temp_list.append(current_list[0])
            elif current_pos in ['determiner', 'wh-determiner']:
                if prev_pos in ['adjective', 'number', 'noun', 'PropN', 'verb', 'particle', 'infinitive_to', 'conjunction', 'pronoun', 'wh-pronoun', 'adverb', 'wh-adverb']:
                    out_list.append(temp_list)
                    temp_list = []
                    temp_list.append(current_list[0])
                else:
                    temp_list.append(current_list[0])
            elif current_pos in ['adjective', 'number']:
                if prev_pos in ['noun', 'PropN', 'verb', 'particle', 'infinitive_to', 'conjunction', 'pronoun', 'wh-pronoun', 'adverb', 'wh-adverb']:
                    out_list.append(temp_list)
                    temp_list = []
                    temp_list.append(current_list[0])
                else:
                    temp_list.append(current_list[0])
            elif current_pos in ['noun', 'PropN']:
                temp_list.append(current_list[0])
            elif current_pos in ['verb', 'particle', 'infinitive_to']:
                if prev_pos in ['verb', 'particle', 'infinitive_to']:
                    temp_list.append(current_list[0])
                else:
                    out_list.append(temp_list)
                    temp_list = []
                    temp_list.append(current_list[0])
            elif current_pos in ['conjunction']:
                out_list.append(temp_list)
                temp_list = []
                temp_list.append(current_list[0])
                out_list.append(temp_list)
                temp_list = []
            elif current_pos in ['pronoun', 'wh-pronoun']:
                out_list.append(temp_list)
                temp_list = []
                temp_list.append(current_list[0])
                out_list.append(temp_list)
                temp_list = []
            elif current_pos in ['adverb', 'wh-adverb']:
                out_list.append(temp_list)
                temp_list = []
                temp_list.append(current_list[0])
                out_list.append(temp_list)
                temp_list = []
            else:  # For words not resolved by POS
                if current_list[0] == 1:
                    cd = "("+current_list[0]+". ##"+current_pos+")"
                    temp_list.append(cd)
                    out_list.append(temp_list)
                    temp_list = []
                else:
                    out_list.append(temp_list)
                    temp_list = []
                    cd = "("+current_list[0]+". ##"+current_pos+")"
                    temp_list.append(cd)
                    out_list.append(temp_list)
                    temp_list = []
        #Last word group is appended in the output_list
        out_list.append(temp_list)
        temp_list = []

        #Removing blank groups from the out_list
        final_list = [current_pos for current_pos in out_list if current_pos]
        out_list = []
        
        #Adding words against their corresponding word ids in group
        for i in final_list:
            for j in i:
                x = word_file[j-1][1]
                temp_list.append(x)
            out_list.append(temp_list)
            temp_list = []
        
        output_path.write(sentence + '\n')
        x = "(E_group (language english) "
        
        for i,k in zip(final_list,out_list):
            y = "(grp_elements_ids "
            z = "(grp_element_words "
            for j in i:
                y = y + str(j) + ' '
            y = y[:-1] + ') '
            for l in k:
                z = z + str(l) + ' '
            z = z[:-1] + '))'
            s = x + y + z
            output_file.write(s + '\n')

        final_out_list = []
        temp_list = []
        y = ""
        for i,k in zip(final_list,out_list):
            counter = 0
            if len(y)!=0:
                y = y[:-1] + "_"
            for j in i:
                x = str(j) + '_' + k[counter]
                y = y + k[counter] + " "
                temp_list.append(x)
                counter += 1
            final_out_list.append(temp_list)
            temp_list = []

        output_path.write('\n' + y + '\n\n')
        outHTML.write(y+'\n')
        for i in final_out_list:
            x = str(i)
            x = x.replace("'","")
            x = x.replace(',',' ')
            output_path.write(x)
            outHTML.write(x)
        output_path.write("\n\n\n")
        
#Calling the function to group words in English
english_group()
