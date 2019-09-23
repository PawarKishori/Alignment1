I To Run_Grouping_Files:
	a. Run: sh Run_Grouping_Files.sh BUgol2.1E

	b. Python Grouping Codes in  this shell files are:
		1. E_Sanity_Check.py
			a. The output files is generated inside the folder of each and every sentence by the name of "E_Sanity_Check.dat".
			b. All the POS information is also stored in a file in the folder containing all the sentences by the name of "E_Sanity_Check_All_Sentences.txt" 
			c. Sentences forwhich sanity check is not done are in the tmp folder by the name "E_Sanity_Log_All_Sentences.txt"
		
		2. E_Grouping_Word_Dependency_Sanity.py:
			a. The output files in facts format is generated inside the folder of each and every sentence by the name of "E_Word_Group_Sanity.dat".
			b. The output files for HTML format is generated inside the folder of each and every sentence by the name of "E_group_HTML_Sanity.dat".
			c. All the grouping information is also stored in a file in the folder containing all the sentences by the name of "E_Word_Group_All_Sentences_Sanity.txt" 

		3. H_Grouping_Word.py:
			b. The output files in facts format is generated inside the folder of each and every sentence by the name "H_Word_Group.dat".
			c. The output files for HTML format is generated inside the folder of each and every sentence by the name of "H_group_HTML.".
			d. All the grouping information is also stored in a file in the folder containing all the sentences by the name of "H_Word_Group_All_Sentences.txt". 
