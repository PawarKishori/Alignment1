#!/bin/bash
END=1000
for i in $(seq 1 $END)
do	
	rename 's/\.\d+/' /home/aishwarya/ILCI/HEALTH_ILCI_parsed/1.$i/H_sentence.$i 
done
