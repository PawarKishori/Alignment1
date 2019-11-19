The code attached below merge the dictionaries. Please find the attached file.

RUN: python <code> <input1> <input2> <output_file>

EX: python /home/user/Downloads/merge_dictionaries.py /home/user/anusaaraka/Anu_data/canonical_form_dictionary/Dictionaries/computer_science_dic_in_canonical_form.txt /home/user/anusaaraka/Anu_data/canonical_form_dictionary/Dictionaries/default-iit-bombay-shabdanjali-dic_smt.txt /home/user/anusaaraka/Anu_data/canonical_form_dictionary/Dictionaries/merged_dictionary.txt

To sort the output file, this is a command line function which will sort the output file in one step:
sort <output_file> -o <output_file>

EX: sort /home/user/anusaaraka/Anu_data/canonical_form_dictionary/Dictionaries/merged_dictionary.txt -o /home/user/anusaaraka/Anu_data/canonical_form_dictionary/Dictionaries/merged_dictionary.txt
