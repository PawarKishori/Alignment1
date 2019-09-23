import os, glob, sys

"""

To run type in terminal - python3 statistics.py BUgol2.1E

"""

path = os.getenv('HOME_anu_tmp') + '/tmp/' + sys.argv[1] + '_tmp/2.*/'
sentences = sorted(glob.glob(path))
outpath = os.getenv('HOME_anu_tmp') + '/tmp/alignment_stats' + sys.argv[1] + '.txt'
out = open(outpath,'w')
out.flush()

store = list()

for sentence in sentences:
	
	try:
		tmp = list()
		facts_resolved = str(sentence) + "save_facts1"
		facts1 = open(facts_resolved).readlines()

		eng_details = str(sentence) + "E_clip_deffact.dat"
		hin_details = str(sentence) + "H_clip_deffact.dat"

		eopen = open(eng_details).readlines()
		hopen = open(hin_details).readlines()

		x = eopen[-1][:-1]
		x = x.replace(')','')
		x = x.split()
		y = hopen[-1][:-1]
		y = y.replace(')','')
		y = y.split()

		E_length = int(x[-1])
		H_length = int(y[-1])
		resolved_eng_length = len(facts1)

		resolved_hin_length = 0

		for i in facts1:
			i = i.split()
			n = len(i) - 2
			resolved_hin_length += n

		percent_eng = round((resolved_eng_length/E_length) * 100, 3)
		percent_hin = round((resolved_hin_length/H_length) * 100, 3)

		m = sentence[36:-1]
		tmp.append(percent_eng)
		tmp.append(percent_hin)
		tmp.append(m)
		
		store.append(tmp)


	except Exception:
		print()
		print("Error at sentence: ", sentence)
		print()


store.sort(reverse=True)

for i in store:
	x = "Sentence: " + str(i[-1]) + '\t\t English % resolved: ' + str(i[0]) + '\t\t Hindi % resolved: ' + str(i[1])
	out.write(x + '\n')
