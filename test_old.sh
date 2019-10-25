#sh test_old.sh ai1E ai1H computer_science

echo "Input files:" $1 $2
cp $1 $HOME_alignment_manju/$1
cp $2 $HOME_alignment_manju/$2

cd $HOME_alignment_manju
source activate python2.7               #irshad's parser needs 2.7
echo "Time taken by alignment_manju module:"
time sh run_alignment.sh $1 $2 $3 nsdp    #$3 = computer_science
echo "End of manju mam's module: "$1 $2
conda deactivate
