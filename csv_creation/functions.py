#Written by Roja(30-10-19)
#Functions needed to create dictionary
############################
#Unique value
def unique_val(val):
    value = []
    lst = val.split('/')
    for each in lst:
        if(each not in value):
            value.append(each)
    return '/'.join(value)

#Creating dic:
def add_data_in_dic(dic, key, val):
    if key not in dic:
        value =  unique_val(val)
        dic[key] = value
    elif(val not in dic[key].split('/')):
        dic[key] = dic[key] + '/' + val

#Return key for a known value:
def return_key(val, dic):
    for key in dic:
        if val == dic[key]:
            return key
        elif val in dic[key].split('/'):
            return key
