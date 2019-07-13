import csv
filename="H_alignment_parserid_invert.csv"
rows=[]
with open(filename,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

lengthrows=len(rows)
column_name=rows[0]
length_column=len(column_name)
f=open("Allfacts.dat","w")
for i in range(1,lengthrows):
    f.write("(Allfacts")
    for j in range(length_column):
        if(rows[i][j]!="_"):
            f.write("("+column_name[j]+" " + rows[i][j] +")")
    f.write(")\n")
f.close()
