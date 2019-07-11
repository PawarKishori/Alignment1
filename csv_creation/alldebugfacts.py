import csv
filename="debug_csv_invert.csv"
rows=[]
with open(filename,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
lengthrows=len(rows)
column_name=rows[0]
length_column=len(column_name)
f=open("Alldebugfacts.dat","w")
for i in range(1,lengthrows):
    str1=""
    temp=0
    for j in range(1,length_column):
        if(rows[i][j]!="."):
            str1=str1+"("+column_name[j]+" " + rows[i][j] +")"
            temp=1
    if(temp==1):
        f.write("(Alldebugfacts ")
        f.write("(A "+str(i)+")")
        f.write(str1)
        f.write(")\n")
f.close()
