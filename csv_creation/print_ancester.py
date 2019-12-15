# Change the path of the file and save.
# To run this program type- python3 print_ancester.py 4
# Here 4 is the node who's child and grand child is to be found.


import sys
fname = str(sys.argv[3])


def get_conll_file():
    file1 = open(sys.argv[1])
    zz = file1.readlines()
    head = []
    word_id = []
    words = []
    new_lst = []
    for i in zz:
        if i != '\n':
            y = i.split("\t")
            y = [elem for l in y for elem in l.split()]
            # print(y)
        word_id.append(y[0])
        words.append(y[1])
        head.append(y[6])
    # print(words)

    node = sys.argv[2]
    z = 1
    if node in head:
        for x in range(len(head)):
            indx = [i for i in range(len(head)) if head[i] == node]
        res_indx = [p + z for p in indx]
        #print(f"child of  {node} is {res_indx}")
        new_lst.append(res_indx)
        #for j in indx:
        #    print(words[j])
        # print(res_indx)
        for i in range(0, len(head)):
            head[i] = int(head[i])

        #check= any(e in head for e in res_indx)
        res_indx1 = []
        res_indx2 = []
        res_indx3 = []
        res_indx4 = []
        res_indx5 = []
        indx1 = []
        indx2 = []
        indx3 = []
        indx4 = []
        indx5 = []
        for i in res_indx:
            if i in head:
                # print(head[i])
                indx1 = [j for j in range(len(head)) if head[j] == i]
                res_indx1 = [p + z for p in indx1]
                # print(res_indx1)
                #print(f"child of {i} is {res_indx1}")
                new_lst.append(res_indx1)
                #for k in indx1:
                #    print(words[k])
                # print(indx1)
                for m in res_indx1:
                    # print(m)
                    if m in head:
                        indx2 = [h for h in range(len(head)) if head[h] == m]
                        res_indx2 = [p+z for p in indx2]
                        #print(f"child of {m} is {res_indx2}")
                        new_lst.append(res_indx2)
                        #for k1 in indx2:
                        #    print(words[k1])
                # print(indx2)

        for s in res_indx2:
            # print(s)
            if s in head:
                indx3 = [h for h in range(len(head)) if head[h] == s]
                res_indx3 = [p+z for p in indx3]
                #print(f"child of {s} is {res_indx3}")
                new_lst.append(res_indx3)
                #for k2 in indx3:
                #    print(words[k2])

                # print(res_indx3)
        for l in res_indx3:
            # print(l)
            if l in head:
                        # print(l)
                indx4 = [h for h in range(len(head)) if head[h] == l]
                res_indx4 = [p+z for p in indx4]
                #print(f"child of {l} is {res_indx4}")
                new_lst.append(res_indx4)
                # print(indx4)
                #for k3 in indx4:
                #    print(words[k3])

#	else:
#		print("no child found")
    par_chl_lst = []
    for each in new_lst:
        if type(each) == list:
            for item in each:
                par_chl_lst.append(item)
        else:
            par_chl_lst.append(each)
    par_chl_lst.sort()
#    print(par_chl_lst)
    new_par_chl_lst = []
    for each in par_chl_lst:
        new_par_chl_lst.append(str(each))
    if new_par_chl_lst != []:
        print('(' + fname + '_parent-sanwawi', node, ' '.join(new_par_chl_lst), ')')
    file1.close()


get_conll_file()
