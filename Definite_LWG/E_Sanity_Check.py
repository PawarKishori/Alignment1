import os, sys, subprocess, glob

"""
Created by	-	Saumya Navneet
Date		-	14/October/2019
Purpose		-	To select one POS out of the given sources.
Input 		-	Enter the path to 'tmp' folder to iterate on all the translated sentences to generate word grouping.
Output 		- 	Inside the folder for every translation, a file 'E_Sanity_Check.dat' will be created containing details of word group, E_Sanity_POS_All_Sentences.txt has POS of all sentences in tmp folder, E_Sanity_Log_All_Sentences.txt contains those sentences for which we are not able to select one single POS.
Files used 	-	E_conll_parse and all_pos_details_combined.dat

For any queries you may drop a message at - saumyanavneet26@gmail.com
"""

class POS:
	def wordnet_pos(self, parser_pos_list, numb):
	
		wordnet = list()
		j=0
		for i in parser_pos_list:
			w = parser_pos_list[j][1]
			word = 'wn ' + w + ' -over'
			out = os.popen(word).readlines()
			temp_pos = list()
			for k in out:
				k = k.split()
				if 'Overview' in k:
					x = k[2]
					if x == 'noun':
						temp_pos.append('NOUN')
					elif x == 'adv':
						temp_pos.append('ADV')
					elif x == 'adj':
						temp_pos.append('ADJ')
					elif x == 'verb':
						temp_pos.append('VERB')
			wordnet.append(temp_pos)
			j += 1
		return(wordnet)


	def gcide_pos(self, parser_pos_list, numb):
	
		gcide = list()
		j=0
		for i in parser_pos_list:
			w = parser_pos_list[j][1]
			word = 'dict ' + w
			out = os.popen(word).readlines()
			temp = list()
			temp_pos = list()
			if len(out) != 0:
				for i in range(len(out)):
					if 'From The Collaborative International Dictionary of English v.0.48 [gcide]:' in out[i]:
						tmp = out[i+2][:-1] + out[i+3][4:-1]
						temp.append(tmp)
				for i in temp:
					if ',' not in i: 
						continue
					x = i.index(',')
					y = i[:]
					if 'a.' in y or 'adj.' in y:
						if 'ADJ' not in temp_pos:
							temp_pos.append('ADJ')
					elif 'adv.' in y:
						if 'ADV' not in temp_pos:
							temp_pos.append('ADV')
					elif 'conj.' in y:
						if 'CONJ' not in temp_pos:
							temp_pos.append('CONJ')
					elif 'comp.' in y:
						if 'COMPOUND' not in temp_pos:
							temp_pos.append('COMPOUND')
					elif 'n.' in y:
						if 'NOUN' not in temp_pos:
							temp_pos.append('NOUN')
					elif 'pref.' in y:
						if 'PREFIX' not in temp_pos:
							temp_pos.append('PREFIX')
					elif 'prep.' in y:
						if 'PREPOSITION' not in temp_pos:
							temp_pos.append('PREPOSITION')
					elif 'p.' in y:
						if 'PARTICIPLE' not in temp_pos:	
							temp_pos.append('PARTICIPLE')
					elif 'subj.' in y:
						if 'SUBJUNCTIVE' not in temp_pos:
							temp_pos.append('SUBJUNCTIVE')
					elif 'superl.' in y:
						if 'SUPERLATIVE' not in temp_pos:
							temp_pos.append('SUPERLATIVE')
					elif 'v.' in y:
						if 'VERB' not in temp_pos:
							temp_pos.append('VERB')
					elif 'vb	n.' in y:
						if 'VERBAL NOUN' not in temp_pos:
							temp_pos.append('VERBAL NOUN')
				gcide.append(temp_pos[:])
				temp_pos.clear()
			else:
				gcide.append(temp_pos)
			j += 1
		return(gcide)

	def sanity_check(self,parser_pos,combined_pos,sanity_outpath,all_sentences,sentence,all_sentences_log):
	
		sanity_output = open(sanity_outpath,'w')
		all_sentences.write("\n" + sentence + "\n")
		x=0

		for i,j in zip(parser_pos,combined_pos):
			if parser_pos[x][0] == combined_pos[x][0] and x < len(parser_pos) :
				wordnet = (combined_pos[x][1])
				gcide = (combined_pos[x][2])
				parser = (parser_pos[x][2])
				word = (parser_pos[x][1])
				relation = (parser_pos[x][3])
				rel_with = (parser_pos[x][4])
				
				pos = []
				temp = 0 
				
				if len(wordnet) != 0 and len(gcide) != 0:
					for i in wordnet:
						for j in gcide:
							if i == j:
								temp = 1
								pos.append(i)
								
				if parser in ["NOUN","VERB","ADJ","ADV"]:			
					if len(wordnet) == 0 :
						if len(gcide) == 0:
							final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(parser_pos[x][2])+"\t"+relation+"\t"+rel_with+"\tPARSER (NPOS)\n"
						elif len(gcide) == 1 and parser != gcide[0]:
							final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(gcide[0])+"\t"+relation+"\t"+rel_with+"\tGCIDE\n"
						elif parser in gcide:
							final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(gcide[0])+"\t"+relation+"\t"+rel_with+"\tPARSER and GCIDE\n"
					elif len(wordnet) == 1 and parser != wordnet[0]:
						final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(wordnet[0])+"\t"+relation+"\t"+rel_with+"\tWORDNET\n"
					else:
						if parser in wordnet:
							final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(parser)+"\t"+relation+"\t"+rel_with+"\tPARSER and WORDNET\n"
						elif temp == 1 and len(pos) == 1: 
							final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(pos[0])+"\t"+relation+"\t"+rel_with+"\tWORDNET and GCIDE\n"	
						elif temp == 1 and len(pos) > 1: 
							final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(pos)+"\t"+relation+"\t"+rel_with+"\tWORDNET and GCIDE (MPOS)\n"
							all_sentences_log.write(sentence + "\n")
						else:
							final_fact = str(parser_pos[x][0])+"\t"+word+"\tERROR \n"	
							all_sentences_log.write(sentence + "\n")
					
				elif parser in ["DET","NUM","PROPN","PUNCT","AUX","PART","CCONJ","SCONJ","CONJ","PRON","ADP"]:
					final_fact = str(parser_pos[x][0])+"\t"+word+"\t"+str(parser_pos[x][2])+"\t"+relation+"\t"+rel_with+"\tPARSER\n"
					
				else:
					final_fact = str(parser_pos[x][0])+"\t"+word+"\tERROR\n"	
					all_sentences_log.write(sentence + "\n")

				sanity_output.write(final_fact)
				all_sentences.write(final_fact)
			x += 1
	
	def exec(self):

		tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
		path = tmp_path + sys.argv[1] + '_tmp'
		path1 = path + '/2.*'
		sentences = sorted(glob.glob(path1))
		
		all_sent = str(path)+'/E_Sanity_POS_All_Sentences.txt'
		all_sent_log = str(path)+'/E_Sanity_Log_All_Sentences.txt'
		open(all_sent, 'w').close()
		open(all_sent_log,'w').close
		all_sentences = open(all_sent,'a')
		all_sentences_log = open(all_sent_log,'a')

		for sentence in sentences:
			print("\n",sentence)
			#Reading the POS information of individual sentences
			conll_path = str(sentence) + '/E_conll_parse'

			pos_details_file = str(sentence) + '/all_pos_details_combined.dat'
			pos_output = open(pos_details_file,'w')
			
			outpath = str(sentence)+'/E_Sanity_Check.dat'
			
			# Reading the files as an input
			english_file = open(conll_path).readlines()
			
			parser_pos_list = list()			#List to extract infromation
			pos_wordnet = list()
			pos_gcide = list()
			final = list()
			temp = list()
			l = list()
			final.clear()
			
			counter = 1
			#Cleaning the file
			for i in english_file:
				if i in ['\n']:
					continue
				else:
					x = i.split("\t")
					l.append(counter)		#Stores element ID
					counter += 1		
					l.append(x[1])			#Stores Word 
					l.append(x[3])			#Stores POS information of the element
					l.append(x[7])
					l.append(x[6])
					parser_pos_list.append(l[:])	#Storing the value in a list to further operate on
					l.clear()			#Clearing the list for further processing 

			pos_wordnet = self.wordnet_pos(parser_pos_list, sentence)
			pos_gcide = self.gcide_pos(parser_pos_list, sentence)
			
			j=0
			
			for i in pos_wordnet:
				temp.clear()
				temp.append(j+1)
				temp.append(pos_wordnet[j])
				temp.append(pos_gcide[j])
				final.append(temp[:])
				j += 1
				
			pos_output.write("[ [WordNet POS]   [Gcide POS] \n\n ")

			for i in final:
				pos_output.write(str(i)+'\n')
				
			self.sanity_check(parser_pos_list,final,outpath,all_sentences,sentence,all_sentences_log)

obj = POS()
obj.exec()
