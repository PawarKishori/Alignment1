#!/bin/bash
END=1000
for i in $(seq 1 $END)
do	
	rm /home/aishwarya/ILCI/HEALTH_ILCI_parsed_final/2.$i/H_sentence.$i
done