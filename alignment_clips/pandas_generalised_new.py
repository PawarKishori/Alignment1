import pandas as pd
import os,sys
import traceback

def starting_function():
    for i in range(len(starting_anchors)):
        numbers_from_starting_anchors = str(starting_anchors[i])
        # print(numbers_from_starting_anchors)
        if((numbers_from_starting_anchors) != '0'):
            print("(anchor_type-english_id-hindi_id anchor ",i+1, " ", numbers_from_starting_anchors, ")")
            new_f.write("(anchor_type-english_id-hindi_id anchor "+str(i+1)+" "+numbers_from_starting_anchors+")\n")
            # starting_anchor_list.append(i)
            unknown_checker.append(i)


def potential_function():
    for i in range(len(potential_anchors)):
        potential_anchor_string = str(potential_anchors[i])
        # print(starting_anchor_list)
        if i not in unknown_checker and (potential_anchor_string) != '0':
            if potential_anchor_string.find("/") is not -1:
                df = potential_anchor_string.split("/")
                for xt in df:
                    xt = xt.split(' ')
                    unknown_checker.append(i)
                    print("(anchor_type-english_id-hindi_id potential ",i+1, " ", " ".join(xt), ")")
                    new_f.write("(anchor_type-english_id-hindi_id potential "+str(i+1)+ " "+ " ".join(xt)+ ")\n")
                    # print(potential_anchor_string.split("#"))
            else:
                    unknown_checker.append(i)
                    print("(anchor_type-english_id-hindi_id potential "+str(i+1)+ " "+potential_anchor_string+ ")")
                    new_f.write("(anchor_type-english_id-hindi_id potential "+str(i+1)+ " "+potential_anchor_string+ ")\n")



def unknown_function():
    for j in range(len(potential_anchors)):
        if j not in unknown_checker:
            print("(anchor_type-english_id-hindi_id unknown "+str(j+1)+" 0)")
            new_f.write("(anchor_type-english_id-hindi_id unknown "+str(j+1)+" 0)\n")


#MAin function--------------------------------------------------------------------------------------------------------------------------------------------------
for k in range(1,125):
    try:
                print()
                print("----------------------------")
                print("2.",k)
                print("----------------------------")
                path_=sys.argv[1]
                path =os.getenv("HOME_anu_tmp")+"/tmp/"+path_+"_tmp/2."+str(k)
                df = pd.read_csv(path+"/All_Resources.csv")
                new_f = open(path+"/Anchor_Facts.dat", 'w')
                row_length = df.shape[0]
                #column_of_names = df.columns.get_loc("Resources")                            #the nth number of column where the anchors' may lie
                column_of_names = df.columns.get_loc("English_word_ids")                            #the nth number of column where the anchors' may lie
                print(column_of_names)
                # print(df.iloc[:,0])
                for i in range(row_length):
                    if((df.iloc[:, column_of_names].tolist())[i]) == "Potential":
                            store_potential = i
                            break
                for i in range(row_length):
                    if((df.iloc[:, column_of_names].tolist())[i]) == "Current":
                            store_start = i
                            break
                potential_anchors = (df.loc[store_potential].tolist())  # Potential Anchors
                print("====>",len(potential_anchors))
                starting_anchors = (df.loc[store_start].tolist())  # Starting Anchors

                potential_anchors = (potential_anchors[1:])  # Removing the 2 starting columns
                starting_anchors = (starting_anchors[1:])  # Removing the 2 starting columns
                print(len(potential_anchors))

                print()
                starting_anchor_list = []
                unknown_checker = []
                starting_function()
                potential_function()
                unknown_function()
                #new_list = [x for x in unknown_checker]
    except Exception:
        path_=sys.argv[1]
        path =os.getenv("HOME_anu_tmp")+"/tmp/"+path_+"_tmp"
        new_ = open(path+"/Anchor_Facts.log", 'a')
        print(traceback.format_exc())
        new_.write("------------------------------------------------------------------"+"\n")
        new_.write("2."+str(k)+"\n")
        new_.write((traceback.format_exc()))
        pass
        
    	

