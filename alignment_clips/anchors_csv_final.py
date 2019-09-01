'''
Objective: To create ordered facts for a given number of sentences(here taken 102(BUgol2.1E))
Input to be Given: the folder name where the input sentences are to given......For example bUgol2.1E
Output to be expected: A file created in each of the folders given below
How to run:



#log files to be created with proper sentence number where there's an error. Add in the except blog a log file named: log_csv2orderedfact.dat
import csv
import os
import re,sys
# new_f=open("nbs_file",'w')


def csv_file_row(input_file):
    with open(input_file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in (readCSV):
                    csv_row.append(row)
    return row

def csv_file_csv_row(input_file):
    with open(input_file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in (readCSV):
                    csv_row.append(row)
    return csv_row

def potential_anchor_generator(input_file):
    #print("sdsd")
    csv_row = csv_file_csv_row(input_file)
    potential_anchor_cleaner = csv_row[:len(csv_row)-2]
    potential_anchor_cleaner = potential_anchor_cleaner[length-4:][0]  # potential anchor------>potential_anchor_cleaner/potential_anchor
    potential_anchor = potential_anchor_cleaner[1:]
    #print(potential_anchor)
    return potential_anchor

def starting_anchor_generator(input_file):
    csv_row = csv_file_csv_row(input_file)
    csv_row = csv_row[:len(csv_row)]
    csv_row = csv_row[length-3:][0]  # starting anchor-------->csv_row/starting_anchor
    starting_anchor = csv_row[1:]
    #print(starting_anchor)
    return starting_anchor

def regex_to_take_numbers(input_file):
    starting_anchor_string = str(input_file[i])
    numbers_from_starting_anchors = str(re.findall('\d+', starting_anchor_string))
    numbers_from_starting_anchors = numbers_from_starting_anchors.replace(",", "").replace("'", "").replace("[", "").replace("]", "")
    return numbers_from_starting_anchors

def unknown_checker_function(row,unknown_checker):
    for j in range(0, len(row)-1):
                if j not in unknown_checker:
                    print("(anchor_type-english_id-hindi_id unknown "+str(j+1)+" 0)")
                    new_f.write("(anchor_type-english_id-hindi_id unknown "+str(j+1)+" 0)")

def potential_checker_function(row,starting_anchor_list,potential_anchor):
    for k in range(0, len(row)-1):
                potential_anchor_string = str(potential_anchor[k])
                # print(potential_anchor_string)
                if k not in starting_anchor_list and (potential_anchor_string) != '0':
                    if potential_anchor_string.find("#"):
                        substring_till_hash_potential_anchor = potential_anchor_string.split('#')
                        for df in substring_till_hash_potential_anchor:
                            df = df.split(' ')
                            saa = ""
                            for sa in df:
                                sa = sa.split('_')
                                saa = saa + " " + str(sa[0])
                        print("(anchor_type-english_id-hindi_id potential "+str(k+1)+saa+")")
                        new_f.write("(anchor_type-english_id-hindi_id potential "+str(k+1)+saa+")")

def starting_anchor_checker_function(row,starting_anchor):
    for i in range(0, len(row)-1):
                starting_anchor_string = str(starting_anchor[i])
                numbers_from_starting_anchors = str(re.findall('\d+', starting_anchor_string))   #regex to take out numbers
                numbers_from_starting_anchors = numbers_from_starting_anchors.replace(",", "").replace(
                    "'", "").replace("[", "").replace("]", "")
                if((numbers_from_starting_anchors) != '0'):
                    print("(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")")
                    new_f.write(
                        "(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")")
                    starting_anchor_list.append(i)
                    #unknown_checker.append(i)
    return starting_anchor_list

if __name__== "__main__":
    temp = sys.argv[1]     #BUgol2.1E
    for l in range(1, 103):
        try:
            input_file = os.getenv(
                "HOME_anu_tmp")+"/tmp/"+temp+"_tmp/2."+str(l)+"/final.csv"
            path = os.getenv("HOME_anu_tmp")+"/tmp/"+temp+"_tmp/2."+str(l)
            new_f = open(path+"/deffact_anchors.dat", 'w+')
            print()
            print("--------------------")
            print("2."+str(l))
            print("--------------------")
            csv_row = []
            starting_anchor_list = []
            row=csv_file_row(input_file)
            csv_row=csv_file_csv_row(input_file)
            print(len(row))
            length = len(csv_row)
            potential_anchor = potential_anchor_generator(input_file)
            starting_anchor = starting_anchor_generator(input_file)
            starting_anchor_list = starting_anchor_checker_function(row,starting_anchor)
            potential_checker_function(row,starting_anchor_list,potential_anchor)
            unknown_checker_function(row,starting_anchor_list)
        except:
            pass

            for i in range(0, len(row)-1):
                starting_anchor_string = str(starting_anchor[i])
                numbers_from_starting_anchors = str(re.findall('\d+', starting_anchor_string))   #regex to take out numbers
                numbers_from_starting_anchors = numbers_from_starting_anchors.replace(",", "").replace(
                    "'", "").replace("[", "").replace("]", "")
                if((numbers_from_starting_anchors) != '0'):
                    print("(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")")
                    new_f.write(
                        "(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")")
                    starting_anchor_list.append(i)
                    unknown_checker.append(i)
            for k in range(0, len(row)-1):
                potential_anchor_string = str(potential_anchor[k])
                # print(potential_anchor_string)
                if k not in starting_anchor_list and (potential_anchor_string) != '0':
                    if potential_anchor_string.find("#"):
                        substring_till_hash_potential_anchor = potential_anchor_string.split('#')
                        for df in substring_till_hash_potential_anchor:
                            df = df.split(' ')
                            saa = ""
                            for sa in df:
                                sa = sa.split('_')
                                saa = saa + " " + str(sa[0])
                        print("(anchor_type-english_id-hindi_id potential "+str(k+1)+saa+")")
                        new_f.write("(anchor_type-english_id-hindi_id potential "+str(k+1)+saa+")")
                        #print(substring_till_hash_potential_anchor)
                        #numbers_from_potential_anchors = (re.findall('\d+', str(substring_till_hash_potential_anchor)))
                        #print(
                        #    "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(numbers_from_potential_anchors)+")")
                        #new_f.write(
                        #    "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(numbers_from_potential_anchors)+")")
                        #total_numbers_from_potential_anchors = (re.findall('\d+', str(potential_anchor_string)))
                        #extra_numbers = ([i for i in total_numbers_from_potential_anchors if not i in numbers_from_potential_anchors or numbers_from_potential_anchors.remove(i)])
                        #print(
                        #   "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(extra_numbers)+")")
                        #new_f.write(
                        #    "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(extra_numbers)+")")
                        unknown_checker.append(k)
                        '''


'''
Objective: To create ordered facts for a given number of sentences(here taken 102(BUgol2.1E))
Input to be Given: the folder name where the input sentences are to given......For example bUgol2.1E
Output to be expected: A file created in each of the folders given below
How to run:
'''


#log files to be created with proper sentence number where there's an error. Add in the except blog a log file named: log_csv2orderedfact.dat
import csv
import os
import re,sys
# new_f=open("nbs_file",'w')
temp = sys.argv[1]     #BUgol2.1E
for l in range(1,103):
    try:
        input_file = os.getenv(
            "HOME_anu_tmp")+"/tmp/"+temp+"_tmp/2."+str(l)+"/final.csv"
        path = os.getenv("HOME_anu_tmp")+"/tmp/"+temp+"_tmp/2."+str(l)
        new_f = open(path+"/deffact_anchors.dat", 'w')
        print()
        print("--------------------")
        print("2."+str(l))
        print("--------------------")
        csv_row = []
        starting_anchor_list = []
        potential_anchor = []
        starting_anchor = []
        unknown_checker = list()
        with open(input_file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in (readCSV):
                csv_row.append(row)
        print(len(row))
        length = len(csv_row)
        potential_anchor_cleaner = csv_row[:len(csv_row)-2]
        potential_anchor_cleaner = potential_anchor_cleaner[length-4:][0]  # potential anchor------>potential_anchor_cleaner/potential_anchor
        potential_anchor = potential_anchor_cleaner[1:]
        csv_row = csv_row[:len(csv_row)]
        csv_row = csv_row[length-3:][0]  # starting anchor-------->csv_row/starting_anchor
        starting_anchor = csv_row[1:]
        #print(potential_anchor)
        #starting_anchor,potential_anchor=potential_anchor,starting_anchor
        #print(starting_anchor)
        #print(potential_anchor)
        for i in range(0, len(row)-1):
            starting_anchor_string = str(starting_anchor[i])
            numbers_from_starting_anchors = str(re.findall('\d+', starting_anchor_string))   #regex to take out numbers
            numbers_from_starting_anchors = numbers_from_starting_anchors.replace(",", "").replace(
                "'", "").replace("[", "").replace("]", "")
            if((numbers_from_starting_anchors) != '0'):
                print("(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")")
                new_f.write(
                    "(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")")
                starting_anchor_list.append(i)
                #print("ssdsds")
                unknown_checker.append(i)
        #print(unknown_checker)
        for k in range(0, len(row)-1):
            potential_anchor_string = str(potential_anchor[k])
            # print(potential_anchor_string)
            if k not in starting_anchor_list and (potential_anchor_string) != '0':
                if potential_anchor_string.find("#"):
                    substring_till_hash_potential_anchor = potential_anchor_string.split('#')
                    for df in substring_till_hash_potential_anchor:
                       df = df.split(' ')
                       saa = ""
                       for sa in df:
                           sa = sa.split('_')
                           saa = saa + " " + str(sa[0])
                       print("(anchor_type-english_id-hindi_id potential "+str(k+1)+saa+")")
                       new_f.write("(anchor_type-english_id-hindi_id potential "+str(k+1)+saa+")")
                    #print(substring_till_hash_potential_anchor)
                    #numbers_from_potential_anchors = (re.findall('\d+', str(substring_till_hash_potential_anchor)))
                    #print(
                    #    "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(numbers_from_potential_anchors)+")")
                    #new_f.write(
                    #    "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(numbers_from_potential_anchors)+")")
                    #total_numbers_from_potential_anchors = (re.findall('\d+', str(potential_anchor_string)))
                    #extra_numbers = ([i for i in total_numbers_from_potential_anchors if not i in numbers_from_potential_anchors or numbers_from_potential_anchors.remove(i)])
                    #print(
                    #   "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(extra_numbers)+")")
                    #new_f.write(
                    #    "(anchor_type-english_id-hindi_id potential "+str(k)+" "+" ".join(extra_numbers)+")")
                    unknown_checker.append(k)
        #print(unknown_checker)
        new_list = [x for x in unknown_checker]
        #print(new_list)
        #print("hjbdsfnmcxz,")
        #print(unknown_checker)
        for j in range(0, len(row)-1):
            if j not in new_list:
                print("(anchor_type-english_id-hindi_id unknown "+str(j+1)+" 0)")
                new_f.write("(anchor_type-english_id-hindi_id unknown "+str(j+1)+" 0)")
    except:
        pass
