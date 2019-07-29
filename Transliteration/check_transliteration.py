###Programme to check whether given words are transliterate words are not.
###Written by Roja (05-11-18)
###Algorithm suggested by Chaitanya Sir
###RUN:: python check_transliteration.py  Eng-word Hindi-word Sound-dictionary
###	 Ex::  python check_transliteration.py  control kaNtrola Sound-dic.txt
###	 To get debug info, RUN::
###	 python check_transliteration.py  -d control kaNtrola Sound-dic.txt
###		(Note: if -d is given then debug info is printed )
############################################################################## 

import sys

############# For debug purpose #############
debug = ''
 
if sys.argv[1] == '-d':
	eng = str(sys.argv[2]).lower()
	hnd = str(sys.argv[3])
	debug = 'ON'
	s = open(sys.argv[4], 'r')
	s_dic = s.readlines()
else:
	eng = str(sys.argv[1]).lower()#.split()
	hnd = str(sys.argv[2])#.split()
	s = open(sys.argv[3], 'r')
	s_dic = s.readlines()

#print debug statements
def print_debug(msg, *var):
	if debug == 'ON':
		print msg , #':::',  
		for i in range(0, len(var)):
			if i != len(var)-1:
				print var[i], 
			else:
				print var[i]

#############################################
#Variables::
sound_dic = {}
eng_index = 0 
hnd_index = 0
count = 0
index = 0
dic_stack = []
stack = []
working_stack = []
cur_e = '-'
cur_h = '-'
final_e_str = ''
final_h_str = ''


###########################################
#Storing Sound dic info in a dic:
for line in s_dic: 
	sound_lst = line.strip().split('\t')
	sound_dic[sound_lst[0]] = sound_lst[1]


#Function to check keys are present in sound dic with each char
def check_key_in_dic(char):
        lst = []
        if char not in sound_dic.keys():
		print_debug('There is no sound starting with this letter', char)	
                exit(0)
        else:
                for key in sound_dic.keys():
                        if key.startswith(char):
                                lst.append(key)
                return lst

print_debug('English string::', eng)	
print_debug('Hindi string::', hnd)	

#Storing sound dic info for current eng keys in dic stack
def store_sound_dic_in_dic_stack(eng_keys):
	for key in eng_keys:
		sound_list = sound_dic[key].split('/')
		for each in sound_list:
			val = key + ' ' + each
			dic_stack.append(val)
	return dic_stack

#Pruning dictionary stack
def prune_dic_stack(en, hn, en_index, hn_index):
	d_stack = []
	for i in range(0, len(dic_stack)):
		e_key = dic_stack[i].split()
		#print e_key
		if ((e_key[0] == en[en_index:en_index+len(e_key[0])]) and (e_key[1] == hn[hn_index:hn_index+len(e_key[1])])):
				d_stack.append(dic_stack[i])
	return d_stack


#Store info in stacks:
#If only one entry in dic stack then store directly into working stack
#Else store last entry in working stack and rest in stack
#In below function:
#s means stack
#w means working stack
#c means complete stack
def store_info_in_stacks(d_stack, e_ind, h_ind, c_e, c_h):
	s = []
	w = []
	c = []
	for i in range(0, len(d_stack)):
		dt=d_stack[i].replace(" ",",")
		if i != len(d_stack)-1:
			c_e = eng[:e_ind]
			c_h = hnd[:h_ind]
			val = c_e + ',' + c_h  + ',' + dt + ',' + str(e_ind) + ','+ str(h_ind)
			s.append(val)
		else:
			c_e = eng[:e_ind]
			c_h = hnd[:h_ind]
			val = c_e + ',' + c_h  + ',' + dt + ',' + str(e_ind) + ','+ str(h_ind)
			w.append(val)
		c.append(s)
		c.append(w)
	return c

#Working area on pop of a stack:
def work_on_pop(s_list, e_index, h_index):
	index_list = []
	a = s_list.pop()
#	print 'Popped value', a
	print_debug('Popped value', a)
	l = a.split(",")
	print_debug('EIndex HIndex', e_index, h_index)
	ei = e_index + len(l[2])
	hi = h_index + len(l[3])
	index_list.append(ei)
	index_list.append(hi)
	print_debug('Index list', index_list)
	return index_list

#Dictionary Stack
def get_dic_stack_info(index):
	e = eng[index]
	
	#To check eng sound exists in sound dic:
	eng_keys = check_key_in_dic(e)
	print_debug('English keys::', eng_keys)

	o = store_sound_dic_in_dic_stack(eng_keys)
	dic_stack = o 
	print_debug('Dictionary stack is:: ', dic_stack)

	dic_stack.sort()
	print_debug('Sorted dictionary', dic_stack)

	#prune dic stack
	out = prune_dic_stack(eng, hnd, eng_index, hnd_index)
	print_debug('Prune dictionary', out)
	print_debug('Length of prune dic', len(out))
	return out


while eng_index < len(eng):
	
	#get dictionary stack info
	o = get_dic_stack_info(eng_index)
	dic_stack = o
	print_debug('Dic stack is::', dic_stack)

	#Storing dic_stack data into stacks:
	out = store_info_in_stacks(dic_stack, eng_index, hnd_index, cur_e, cur_h)
	print_debug('Complete stack' , out, stack, working_stack)
	dic_stack = []

	if len(out) > 1:
		stack = out[0]
		working_stack = out[1]
		print_debug('Stacks are::' , stack, working_stack)
		o = work_on_pop(working_stack, eng_index, hnd_index)
		eng_index = o[0] 
		hnd_index = o[1]
		print_debug('Current index is::', eng_index, hnd_index)
	else:
		if len(stack)>0:
			a = stack.pop()
			working_stack.append(a)
			print_debug('Working_stack is::', working_stack, type(working_stack))
			l = a.split(",") #To get current eng index and hindi index
			#print l
			o = work_on_pop(working_stack, int(l[4]), int(l[5])) # Ex: trehan  wrehana
			eng_index = o[0] + 1 
			hnd_index = o[1] + 1
			print_debug('Current index is::', eng_index, hnd_index)
		else:
			print("no match")
			exit()

	final_e_str = eng[:eng_index]
	final_h_str = hnd[:hnd_index]
	print_debug('Final string is::', final_e_str , final_h_str)

################################
#Check transliteration::
if final_e_str == eng and final_h_str == hnd:
	print 'Given word is transliterate word'
elif final_e_str == eng and final_h_str + 'a' == hnd:
	print 'Given word is transliterate word'
