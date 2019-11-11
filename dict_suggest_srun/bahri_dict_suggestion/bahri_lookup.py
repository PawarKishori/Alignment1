# this program will run in the second iteration of alignment to suggest english words
# for the leftover hindi words using bahri dictionary.

#packages
import re
import sys
import os
import glob

# bahri dictionary is originally available in utf8 encoding.
# since the hindi words stored in the file is in wx format, the bahri dictionary
# was converted to wx format to make it compatible with my code
# the following function takes out the first word of the each line in the bahri dictionary and
# stores it as key and the remaining words as value in the python dict 'bahri_dict'
def make_bahri_dict():
    bahriHIN_ENG = open('bahri_hin_eng','r').readlines()
    print('Creating dictionary')
    bahri_dict = dict()
    for i in bahriHIN_ENG:
        t = i.split(' ')
        gloss = ' '.join(t[1:])
        bahri_dict[t[0]]=gloss
    return bahri_dict

# the following function is called for each of the left over hindi words
# the hindi word is then looked up in the key part of the bahri_dict if a match is found
# it searches for the english word in the value part of bahri_dict
def bahri_lkup(bahri_dict,h_word,e_words,output):
    #open output file in write mode and write the final result
    Out_File = open(output,'w')
    for key,value in bahri_dict.items():
        # suggested_Ewords = ''
        if h_word == key:
            for e in e_words:
                if e in value and e.lower() not in ['on','to','of','the','a'] and len(e)>1:
                    print(h_word+' <> '+e)
                    Out_File.write(h_word + ' <> ' + e + '\n')
                    break
    Out_File.close()


# this is the main function which is compatible with any corpus
# we just have to enter the name of the corpus tmp directory while running the program
def __main__():
    # converting from list to dict data type
    bahri_dict = make_bahri_dict()
    # path to the tmp directory
    tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
    path = tmp_path + sys.argv[1] + '_tmp'
    path = path + '/2.*'
    sentences = sorted(glob.glob(path))
    # running for each folder
    for sentence in sentences:
        try:
            hindi_left_over = open(str(sentence)+'/hindi_leftover_words_utf.dat','r').readline()
            english_left_over = open(str(sentence)+'/english_leftover_words.dat','r').readline()
            if len(hindi_left_over) > 0 and len(english_left_over) > 0:
                hindi_left_over_words = hindi_left_over.split(' ')
                english_left_over_words = english_left_over.split(' ')
                print("\n" + str(sentence))
                print("left over hindi words: ", hindi_left_over)
                print("left over english words: ", english_left_over)
                for h_word in hindi_left_over_words:
                    output = str(sentence) + '/srun_bahri_dict_suggestion.dat'
                    bahri_lkup(bahri_dict,h_word,english_left_over_words,output)
        except FileNotFoundError:
            print("all hindi words aligned")


if __main__():
    __main__()
