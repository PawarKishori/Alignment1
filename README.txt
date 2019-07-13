README for H_Createdata.py and H_Modules.py

PURPOSE: 
1. Creates tree for given conllu file
2. Corrects errors in parser - OBL and CC 
3. Modifies the vibhakti and tam information, generates files for storing facts and update relation to generate new tree

FILES/LIBRARIES TO IMPORT:
1. wxconv
2. numpy
3. pandas 
4. anytree

PRE-REQUISITE FILES NECESSARY:
1. Vibhakti file (List of all vibhakti's) - Used in obl_err , lwg functions - Path must be changed according to user's requirement 
2. revised_manual_local_word_group.dat or manual_local_word_group.dat - Used in tam_and _vib_lwg function to provide necessary TAM groupings - Path must be in 																			path_des of user
3. H_sentence - Used in both punct_info and lwg functions 

CODE FLOW:
1. Segment1: Accepting Fielname and path (loops over all files in directories)
	1) input path: Enter path till directory where all directories reside (Ex: /home/aishwarya/GeoE01_tmp)
	2) filename: Particular directory to which conllu file belongs (Ex: 2.2)
	3) path_des: path + filename (Ex: /home/aishwarya/GeoE01_tmp/2.2)
	4) parse: path_des + conllu file (Ex: home/aishwarya/GeoE01_tmp/2.2/hindi_dep_parser_original.dat)

2. Segment2: Creating dataframe
	1) Call create dataframe function from H_Modules.py to create dataframe from given conllu file (Ex: H_Modules.create_dataframe(parse, path, filename))

3. Segment3: Removing all punctuations

4. Segment4: Updating PID and PIDWITH
	1) Call data_PID_PIDWITH to modify the PID and update existing PIDWITH's (Ex: H_Modules.data_PID_PIDWITH_mod(relation_df, dflen, path, filename))
	   Here, dflen refers to the length of the dataframe

5. Segment5: Creating dictionary 
	1) Call function to create dictionary (H_Modules.create_dict(relation_df))

6. Segment6: Change wx to utf format by calling function
	1) Call function to append column with utf word corresponding to wx word in relation_df	
	2) Old dataframe is stored in relation_old_df

7. Segment7 : Call function to create string as json
	1) H_clause_single_line_words_initial - Holds the json string to form string (uses a recursive function to produce DFS traversal)

8. Segment8 : Call function to draw tree (Ex: H_Modules.drawtree(string, path_des, path, file)) 

9. Segment9 : Correct OBL and CC errors (Ex: H_Modules.obl_err(relation_df, sub_tree, path, filename) (Ex: H_Modules.conj_cc_resolution(relation_df, stack, sub_tree, 				path, filename))

10. Segment10 : Repeat Segment7 to generate new string once OBL and CC corrections are made and then call function to draw updated tree 

11. Segement11 : Call function that generates a file to save all local word groupings in the sentence (Ex: H_Modules.lwg(path_des, path, filename))

12. Segment12 : Call function to create local word grouping using generated vibhakti file and pre-existing TAM file (Ex: H_Modules.tam_and_vib_lwg(error_flag, 					sub_tree, relation_df, path, path_des, filename))

13. Segment13: Call function to create dictionary and update UTF conversion

14. Segment14: Once again, function to generate string and tree is called to generate final updated tree (After Vib and TAM  corrections)

15. Segment15: Generate Wordid-word mappings and store in a file, generate parserid-wordid mappings and store in another file. Both files are stored in fact 				   format. (Ex: H_Modules.wordid_word_mapping(path_des, relation_df), H_Modules.parserid_wordid_mapping(path_des, relation_df))

16. Segment16: Call function to save punctuation information (Since it is being deleted from the tree and dataframe) (Ex: H_Modules.punct_info(path_des, 						   relation_df, relation_old_df, path, filename))

17. Segment17: The DFS traversal of the file (tree) is stored in another file.

H_Modules.PY:
List of functions in H_Modules.py:
1) create_dataframe - Creates dataframe
2) data_PID_PIDWITH_mod - Converting PID to WID and find corresponding PIDWITH's
3) create_dict - Creates dictionary
4) wx_utf_converter_sentence - Converts data in wx format to utf format
5) wx_utf_converter - Appends UTF format column to main dataframe
6) form_final_json_tree - Function to form final json string
7) drawtree - Creates the tree 
8) obl_err - Corrects OBL errors
9) BFS - Performs BFS traversal
10) conj_cc_resolution - Corrects CC-CONJ errors
11) lwg - Gnenerates file to store local word grouping facts for vibhakti
12) tam_and_vib_lwg - Creates local word grouping for TAM and vibhakti and updates relation_df and dictionary
13) wordid_word_mapping - Performs wordid-word mapping and stores as facts
14) parserid_wordid_mapping - Performs punctid-wordid mapping and stores as facts
15) punct_info - Stores punctuation information
16) DFS - Performs DFS raversal and saves file as facts

FILES GENERATED:
1. H_tree_initial.png - Stores tree generated in Segment8 (stored in path_des)
2. obl_errors_log - Stores log of changes/errors in OBL corrections in fact format (stored in path)
3. cc_errors_log.dat - Stores log of changes/errors generated during CC-CONJ corrections in fact format (stored in path)
4. cc_list - Contains list of all CC occurrences in the sentence
5. H_tree_corrected.png - Stores corrected tree generated in Segment10 (stored in path_des)
6. H_def_lwg-wid-word-postpositions_new - Stores all local word groupings of vibhakti's in fact format (stored in path_des)
7. tam_vib_error_log - Stores log of errors in tam and vibhakti, ie., when the node to be removed has children (stored in path)
8. H_tree_final.png - Stores final tree generated in Segment14 (stored in path_des)
9. H_wordid-word_mapping.dat - Stores mapping of word-d-word in fact format (stored in path_des)
10. H_parserid-wordid_mapping.dat - Stores mapping of parserid-wordid in fact format (stored in path_des)
11. H_punc-pos-ID - Stores punctuation information corresponding to every sentence (stored in path_des)
12. H_log - Log of all general errors in the whole process (stored in path)