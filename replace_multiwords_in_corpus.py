#python replace_multiwords_in_corpus.py cl_hindi_100_detok /home/user/forked/anuAlignment
import sys
#corpus_file_path="/home/user/forked/alignment_manju"
corpus_file_path=sys.argv[2]
def main():
	mwe_dict_eng=[]
	mwe_dict_hnd=[]
	with open(corpus_file_path+"/"+sys.argv[1],"r") as g:
		corpus = g.read()

	for line in open ("Geo_multi_H2E.txt","r"):
		mwe_dict_hnd.append(" ".join((line.strip().split('\t')[0].split("_"))))
		#mwe_dict_eng.append(" ".join((line.strip().split('\t')[1].split("_"))))		
	#print (mwe_dict_hnd[5])

	for mwe in mwe_dict_hnd:
		corpus=corpus.replace(mwe,mwe.replace(" ","_"))
	with open(corpus_file_path+"/"+sys.argv[1]+"_multiwords_underscored","w") as g:
		g.write(corpus)
	g.close()
	print(sys.argv[1]+"_multiwords_underscored")

if __name__ == '__main__':
	main()
