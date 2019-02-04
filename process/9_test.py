#!/usr/bin/python3


#f = open("tmp.txt")
#
#lines = f.readlines()
#
#sup_lines = list(set(lines))
#for line in sup_lines:
#    print(line.split('\t')[0].strip() + "\t" + line.split('\t')[1].strip().split('.')[0].split('-')[0])




f = open("tmp2.txt")

lines = f.readlines()
sup_lines = list(set(lines))

#companies = []
for line in sup_lines:
    #companies.append(line.split('\t')[0])
    print(line.split('\t')[0].strip() + "\t" + line.split('\t')[1].strip().split('.')[0].split('-')[0])

#print(set([x for x in companies if companies.count(x) > 1]))

    
