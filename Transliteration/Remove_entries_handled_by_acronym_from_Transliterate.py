import sys, os

transliterate_new = os.getenv('HOME_alignment')+'/Transliteration/dictionary/lookups'+'/Lookup_transliteration_final_AI_all_eng.txt'
transliterate_old = os.getenv('HOME_alignment')+'/Transliteration/dictionary/lookups'+'/Lookup_transliteration_AI_all_eng.txt'
acronym = os.getenv('HOME_alignment')+'/Transliteration/dictionary/lookups'+'/Lookup_transliteration_acronymAI_all_eng.txt'

with open(acronym,"r") as f:
    a = f.read().split("\n")
    while "" in a:
        a.remove("")
    #a_eng = [x.split(" <> ")[0] for x in a]

with open(transliterate_old,"r") as f:
    t = f.read().split("\n")
    while "" in t:
        t.remove("")


print(a)
print("--")
print(t)
print("--")

print("Initial:",len(t))
for x in a:
    for y in t:
        if (x.split(" <> ")[0]==y.split(" <> ")[0]):
            print(x,y)
            t.remove(y)
print("Final:",len(t))

with open(transliterate_new, "w") as f:
    for i in t:
        f.write(i+"\n")
 
