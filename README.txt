Alignment1 module pipeline:

The three packages ran in final alignment are in the following sequence:
1. anusaaraka
2. alignment_manju
3. Alignment1

Path to set in bashrc: 

$HOME_alignment = path to Alignment1
$HOME_alignment_manju = path to alignment_manju

To run whole alignment(i.e anusaaraka, alignment_manju, Alignment) run following command:
sh run_package.sh Eng Hnd_wx
(Note: The parallel files should be copied in alignment_manju folder)

To run specific module in Alignment1:
sh working_debug/test3.sh ai1E
(You can't run test3.sh inside working_debug, you need to run it from Alignment1/ . The reason to run a specific module's shell from Alignment1/ is that the english file which is used in the shell in $1 argument is present in Alignment1/ )


