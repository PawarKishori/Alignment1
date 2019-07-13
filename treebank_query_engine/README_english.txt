README for Query Engine for English Treebank Database
----------------------------------------------------------------------------------------------------------------------------------------

1.queries_english.py:
	(i)The above python file is used to generate query and access the database Treebank_English.db(The English Treebank). Open the 		   terminal and type the following command to run the above python file.
			python queries_english.py
	
	(ii) You will get the following options once the python program is run:
		1.No of words in a sentence
		2.No of minor field types and information
		3.POS combinations and respective records
		4.Identify parent(word) corresponding to each word in a given sentence
		5.To find the word and it's gender in a given sentence
		6.To obtain information about a given relation, including corresponding POS's and sentences
		7.To obtain sibling relations in a given sentence
		8.To obtain Noun followed by verb cases and print relation
		9.Quit 

      	    Please select one of the options(1-9)
  	(iii) If you had selected:
		OPTION 1 :
	 	This basically gives the no of words in a sentence.

		So just input the Sentence No. for which you want to know the no. of words.You will get the no of words once you input the 			sentence id.
  		----------------------------------------------------------------------------------		
		OPTION 2:
		This query gives all the minor field types of a morphological type that exist in the database, and the words of the database 			of a certain field type, if needed.
		
		Initially you have to input one of the following options as input:
		
		Definite,PronType,Number1,Mood,Person,Tense,VerbForm,NumType,Degree,Case1,Gender1,Poss,Foreign1,Voice,Reflex,Typo,Abbr
		
		The minor field types will be displayed on the terminal along with the number of occurences.		
		Next, Press 'Y' or 'y' if you want to view the words for a particular field type. Else,press any other key.
		If you had pressed 'y' or 'Y', then enter the field type for which you want to view the words.
		The words for the entered type will be stored in the file 'morphdetails_english.txt'(stored in the same directory as your 			query program file).
		----------------------------------------------------------------------------------
		OPTION 3:
		This option gives the different types of pos_UD and pos_ILMT pairs, and the no of occurrences of each type. Also, one can 			choose to view the words of a certain pair of pos_UD and pos_ILMT.
		
		All the types of pos_UD and pos_ILMT pairs are displayed first, along with the number of occurrences.Press 'Y' or 'y' if you 			want to view the words belonging to a certain type. Enter the pos_UD and pos_ILMT type, and you can view the words in the file 			'UD-ILMT_occurrence_english.txt'(stored in the same directory as your query program file).
		----------------------------------------------------------------------------------
		OPTION 4:
		This gives the parent for every word in a given sentence.

		The user has to input the sentence-id and the word-parent pairs will be stored in a file named 
		'word-parent_english.txt'(stored in the same directory as your query program file).
		------------------------------------------------------------------------------------
		OPTION 5:
		This gives word and it's gender in a given sentence.

		The user has to input the sentence-id and the word and it's gender will be stored in a file named 
		'Word-Gender_enflish.txt'(stored in the same directory as your query program file).
		--------------------------------------------------------------------------------------
		OPTION 6:
		This option gives the POS of the child and the parent and the no of occurrences of each type. Also the parent-child pairs for 			a case obtained if the user wishes to.

		The user has to input the relation required, and types of POS of child and parent along with no of occurrences is printed in 			the terminal. Press 'y' or 'Y' if you want to view word by word cases of a given type.Else, press any other key.
		Now, enter the POS of parent and child. All word by word cases of the required type will be in the file 		'relation_to_word_mapping_english.txt'(stored in the same directory as your query program file).
		---------------------------------------------------------------------------------------
		OPTION 7:
		This option is to print the parent and the SentenceId for two user input relations of two siblings with their parent.

		All the relations that exist in the document will be displayed in the terminal and the user has to choose any two relations for
		which he/she wishes to check sibling relationship. The output will be the filename and the corresponding parent-id in the 			terminal.
		---------------------------------------------------------------------------------------
		OPTION 8:
		This is to find all cases in which the noun is followed by verb, and the relation that exists between the noun and the verb.
		
		The file 'noun-verb_english.txt' will contain the noun and the verb(where noun is succeeded by verb) along with the relation 			that exists between them.
		---------------------------------------------------------------------------------------
		OPTION 9:
		This option is to quit the query search engine.
		---------------------------------------------------------------------------------------

	(iv) You will get an option whether to continue accessing the query engine or not. Press 'Y' or 'y' to continue and 'N' or 'n' 		     to	quit the engine.

	    On pressing 'Y' Or 'y', you will go back to step 1.(ii).
-----------------------------------------------------------------------------------------------------------------------------------------
			
		
