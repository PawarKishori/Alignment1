import glob
import os, sys
"""
Created by	-	Prashant Raj & Saumya Navneet
Date		-	30/August/2019
Purpose		-	To generate local groups based on POS information to help in word alignment.
Input 		-	Enter the path to 'tmp' folder to iterate on all the translated sentences to generate word grouping.
Output 		- 	Inside the folder for every translation, a file 'E_Word_Group.txt' will be created containing details of word group.
Files used 	-	E_conll_parse

For any queries you may drop a message at - prashantraj012@gmail.com or saumyanavneet26@gmail.com
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
	

	for sentence in sentences: 	#Change according to the number of sentences
		
		#Reading the conll parser information of individual sentences
		conll_path = str(sentence) + '/E_conll_parse'
		
		#Reading the file as an input
		englishfile = open(conll_path).readlines()
		outpath = str(sentence)+'/E_Word_Group.txt'
		outpathHTML = str(sentence) + '/E_group_HTML.txt'
		outHTML = open(outpathHTML,'w')
		outHTML.flush()
		output_file = open(outpath,"w")
		output_file.flush()
		eng = list()				#Temporary list to extract infromation
		l = list()					#Helper list
		counter = 1
		
		#Cleaning the file
		for i in englishfile:
			if i in ['\n']:
				continue
			else:
				x = i.split("\t")
				if x[3] == 'PUNCT':
					continue
				else:
					l.append(counter)
					counter += 1		#Stores element ID
					l.append(x[3])		#Stores POS information of the element
					l.append(x[1])		#Stores the actual word element
					l.append(x[7])		#Stores relation of word with it's head
					eng.append(l[:])	#Storing the value in a list to further operate on
					l.clear()		#Clearing the list for further processing

		out_list=list()				#To store the local word groups
		temp_list=list()			#Used to generate local word groups
		
		i = 0
		while i < len(eng):
			current_pos = eng[i][1]
			current_word = eng[i][2]
			prev_pos = ""
			next_word = ""
			prev_word = ""
			prev_rel = ""
			counter = i
			
			if i < len(eng)-1:
				next_word = eng[i+1][2]
				
			if i != 0:
				prev_pos = eng[i-1][1]
				prev_word = eng[i-1][2]
				prev_rel = eng[i-1][3]
				
			if current_pos in ["ADP"]:
				if current_word in ["to"]:
					if prev_word in ["Due","due","According","according"]:
						temp_list.append(eng[i][0])
				elif prev_pos in ["DET","ADJ","NUM","NOUN","PROPN","PUNCT","AUX","VERB","PART","CCONJ","SCONJ","CONJ","PRON","ADV"]:
					out_list.append(temp_list[:])
					temp_list.clear()
					temp_list.append(eng[i][0])
				else:
					temp_list.append(eng[i][0])
					
			elif current_pos in ["DET"]:
				if current_word in ['A', 'An', 'The', 'a', 'an', 'the']:
				        temp_list.append(eng[i][0])
				        while current_pos not in ['NOUN', 'PROPN'] and (counter < (len(eng)-1)):
				            counter += 1
				            current_pos = eng[counter][1]
				            temp_list.append(eng[counter][0])
				        i = counter      
				elif prev_pos in ["ADJ","NUM","NOUN","PROPN","PUNCT","AUX","VERB","PART","CCONJ","SCONJ","CONJ","PRON","ADV"]:
					out_list.append(temp_list[:])
					temp_list.clear()
					temp_list.append(eng[i][0])
				else:
					temp_list.append(eng[i][0])
					
			elif current_pos in ["ADJ","NUM"]:
				if prev_pos in ["NOUN","PROPN","PUNCT","PRON","AUX","VERB","PART","ADV","CCONJ","SCONJ","CONJ"]:
					out_list.append(temp_list[:])
					temp_list.clear()
					temp_list.append(eng[i][0])
				else:
					temp_list.append(eng[i][0])
					
			elif current_pos in ["NOUN","PROPN"]:
				if prev_pos in ["NOUN","PROPN"] and prev_rel in ["compound"]:
					temp_list.append(eng[i][0])
				elif prev_pos in ["DET","ADJ","NUM","ADP"]:
					temp_list.append(eng[i][0])
				else:
					out_list.append(temp_list[:])
					temp_list.clear()
					temp_list.append(eng[i][0])
					
			elif current_pos in "PUNCT":
				continue
		
			elif current_pos in "SYM":
				temp_list.append(eng[i][0])

			elif current_pos in ["VERB","AUX","PART"]:
				if prev_pos in ["VERB","AUX","PART"]:
					temp_list.append(eng[i][0])
				else:
					out_list.append(temp_list[:])
					temp_list.clear()
					temp_list.append(eng[i][0])
					
			elif current_pos in ["CONJ","CCONJ","SCONJ","PRON","ADV"]:
				out_list.append(temp_list[:])
				temp_list.clear()
				temp_list.append(eng[i][0])
				out_list.append(temp_list[:])
				temp_list.clear()

			else:
				if i == 0:
					temp_list.append(eng[i][0])
					temp_list.append(999)		#For elements not resolved through POS
					out_list.append(temp_list[:])
					temp_list.clear()
				else:
					out_list.append(temp_list[:])
					temp_list.clear()
					temp_list.append(eng[i][0])
					temp_list.append(999)		#For elements not resolved through POS
					out_list.append(temp_list[:])
					temp_list.clear()
			i = i+1
			
		out_list.append(temp_list[:])		#Last local group for the sentence appended
		temp_list.clear()					#List cleared for further processing
		
		
		final_list = [ current_pos for current_pos in out_list if current_pos ]		#For removing the empty word groups generated
		output = list()						#List for storing values with actual words
		
		
		for i in final_list:
			for j in i:
				if j == 999:
					temp_list.append("##")		#For displaying unresolved indices	
				else:
					x = eng[j-1][2]
					temp_list.append(x)		#For appending resolved indices
			output.append(temp_list[:])			#For appending local group to the output list
			temp_list.clear()				#Clearing the temp list for further computation
		
		output_path.write(sentence + '\n')

		x = "(E_group (language english) "
		for i,k in zip(final_list,output):
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
		output_path.write('\n\n')


		final_out_list = []
		temp_list = []
		y = ""
		for i,k in zip(final_list,output):
			counter = 0
			if len(y)!=0:
				y = y[:-1] + " "
			for j in i:
				x = str(j) + ' ' + k[counter]
				y = y + k[counter] + "_"
				temp_list.append(x)
				counter += 1
			final_out_list.append(temp_list)
			temp_list = []
			
		output_path.write('\n' + y + '\n\n')
		outHTML.write(y + '\n')
		
		for i in final_out_list:
			x = str(i)
			x = x.replace("'","")
			x = x.replace(',',' ')
			output_path.write(x)
			outHTML.write(x)
		output_path.write("\n\n\n")
		
#Calling the function to group words in English
english_group()
