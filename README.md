Steps to run Alignment1:

[Note: Depending on the code's dependency (python2/python3) I have activated the conda sessions in the following shells.
name for python3 env in the shell used is "py3.6" and for python2 it is "python2.7". Kindly create these environmrnts in your machine too.]

1. Runing anusaaraka and alignment_Manju
   sh test_old.sh ai1E ai1H computer_science

   note: ai2H should be in wx
         ai2E and ai3E preprocessed as per the steps of preprocessing/todo

2. Running main Alignment1 module
   sh new_test.sh ai1E ai1H

=========================================================

Before 1 and 2, a) and b) must be done.

a) Running Termsuit, downloading dictionaries from Bharatawani, Collins etc. 
   Seperatly has to be done by Nupur and give me the dictionaries for the domain.

b) Running Alignment1's pre module (The codes which runs on whole corpus at a time and creates lookup small dictionaries, which will be used by further modules)
   (Shell is not generalised yet)
   sh Preprocessing.sh AI_all_eng All_all_hin

