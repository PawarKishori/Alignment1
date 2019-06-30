#!/bin/bash
END=1000
for i in $(seq 1 $END)
do	
	mv /home/aishwarya/ILCI/HEALTH_ILCI_parsed_final/2.$i/H_sentence /home/aishwarya/ILCI/HEALTH_ILCI_parsed_final/1.$i
	rm -r /home/aishwarya/ILCI/HEALTH_ILCI_parsed_final/2.$i
done