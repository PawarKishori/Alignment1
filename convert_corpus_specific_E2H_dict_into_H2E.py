import sys
def main():

	#f2=open(sys.argv[3], 'w')	#single_word_dict
	#f3=open(sys.argv[3], 'w')	#multi_word_dict
	def finding_the_difference_between_2_lists(lst1, lst2): 
		lst3 = [value for value in lst1 if value not in lst2] 
		return lst3 ;

	def E2H_to_H2E(E2H_dict_name,H2E_dict_name):
		dict_list=[]
		H2E_list_temp=[]
		H2E_list=[]
		temp1=[]
		temp2=[]
		f1=open(E2H_dict_name, 'r')
		f2=open(H2E_dict_name, 'w')
		#Creating H2E_list (has duplicate tuples)
		for line in f1:
			if line=='\n':continue
			else:
				eword=line.split('<=>')[0].strip()
				hindi_words=line.split('<=>')[1].strip()
				for hword in hindi_words.split('/'):
					if len(hword)==0: print("Hindi val missing in dict for "+eword)
					else: dict_list.append((hword.replace(' ','_'),eword.replace(' ','_')))
		f1.close()

		#Creating H2E_list with unique tuples but first column of some tuples still have same value
		H2E_list=sorted((list(set(dict_list))))
		#Combining tuples having same first col value; the columns other than first are concatenated with '/'
		for x in H2E_list:
			if x[0] not in temp1:
				temp1.append(x[0])
				temp2.append(x[1])
				H2E_list_temp.append((x[0],x[1]))	#This list has the first occurence of every hindi word

		H2E_list=finding_the_difference_between_2_lists(H2E_list, H2E_list_temp)
		for y in H2E_list:
				if y[0] in temp1:
					i=temp1.index(y[0])
					temp2[i]=temp2[i]+"/"+y[1]
		dict_list=[]
		for i in range(len(temp1)): 
			dict_list.append((temp1[i],temp2[i]))

		dict_list = sorted(dict_list, key=lambda x:(len(x[0].split("_")),x),reverse=True)
		#print dict_list
			#Writing the dictionary to a file
		for j in dict_list:
			f2.write("\t".join(j)+"\n")
		f2.close();

	E2H_to_H2E(sys.argv[1],sys.argv[2])	
	E2H_to_H2E(sys.argv[3],sys.argv[4])

if __name__ == "__main__" : main()



