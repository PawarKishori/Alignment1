Steps to run Alignment1:

[Note: Depending on the code's dependency (python2/python3) I have activated the conda sessions in the following shells and enherently called shells.
name for python3 env in the shell used is "py3.6" and for python2 it is "python2.7". Kindly create these environmrnts in your machine too.

For those who does not  have Anaconda, kindly call python3 and python2 whereever I have  activated py3.6 or python2 env respectively.
And remove "source activate _ " and "conda deactivate" from the shell scripts in the Alignment1 repository.
]


1. Runing anusaaraka and alignment_Manju
   sh test_old.sh ai1E ai1H computer_science

   note: ai2H should be in wx
         ai2E and ai3E preprocessed as per the steps of preprocessing/todo

2. Running main Alignment1 module
   sh new_test.sh ai1E ai1H

=========================================================

Before 1 and 2, a) and b) must be done. [For AI corpus a) and b) steps are done by me and generated lookup dictionries which are used in 1. and 2.]

a) Running Termsuit, downloading dictionaries from Bharatawani, Collins etc. 
   Seperatly has to be done by Nupur and give me the dictionaries for the domain.

b) Running Alignment1's pre module (The codes which runs on whole corpus at a time and creates lookup small dictionaries, which will be used by further modules)
   (Shell is not generalised yet)
   sh Preprocessing.sh AI_all_eng All_all_hin

