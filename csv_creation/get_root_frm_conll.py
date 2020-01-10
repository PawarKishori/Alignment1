import sys

for line in open(sys.argv[1]):
    if line != '\n':
        lst = line.strip().split('\t')
        rt = lst[2]
        print('(id-conll_root', lst[0], rt, ')')
