#!/usr/bin/python3


f = open("../data/members/lawyers_text_by_exam.txt")
f_list = open("../data/members/lawyers.txt")

l_list = f_list.read().replace('\n',' ')

while True:
    line = f.readline()
    if not line: break

    if line.strip() not in l_list:
        print(line.strip())
    
