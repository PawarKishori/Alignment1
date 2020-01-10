import sys

lab = str(sys.argv[2])

for line in open(sys.argv[1]):
    lst = line.strip().split('\t')
    print('(' + lab +'_relation_name-head-chiid', lst[7], lst[6], lst[0], ')')
