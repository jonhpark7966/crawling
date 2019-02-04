#!/usr/bin/python3
# -*- coding: utf-8 -*-


def add_space_to_careers(career):
    return career.replace("법무법인", " 법무법인 ").replace("법률사무소", " 법률사무소 ").replace("(", " (").replace(")", " ) ")

def find_id(infos):
    candidate = []

    lawyers_file = '../data/members/lawyers.txt'
    infos[4] = "."
    f_sid = open(lawyers_file)
    for sid in f_sid.readlines():
        pop = False 
        for line in open("../data/lawyers0/" + sid.rstrip()):
            if infos[3] not in line: #name is not in file
                break  
            candidate.append(line)
            if pop is True:
                candidate.pop()
            pop = True

            # name in in file && career match
            if (" " +infos[0].strip()+" ") in (" " + add_space_to_careers(line.split('\t')[17].strip())+" "):
                #print(infos[0].strip() + " / " + add_space_to_careers(line.split('\t')[17].strip()))
                #company is in file
                infos[4] = line.split('\t')[1].strip()
                infos[6] = line.split('\t')[2].strip()
                infos[7] = line.split('\t')[3].strip()


    if len(candidate) == 1 and infos[4] == ".":
        infos[4] = candidate[0].split('\t')[1].strip()
        infos[6] = candidate[0].split('\t')[2].strip()
        infos[7] = candidate[0].split('\t')[3].strip()
    elif len(candidate) > 1 and infos[4] == ".":
        found = 0
        for i in range(len(candidate)):
            if "판사" in candidate[i] or "검사" in candidate[i]:
                found = found + 1
            else:
                infos[4] = candidate[0].split('\t')[1].strip()
                infos[6] = candidate[0].split('\t')[2].strip()
                infos[7] = candidate[0].split('\t')[3].strip()
#        if len(candidate) - found > 1:
            #print("MULTIPLE Candidate: " + infos[0] + " / " + infos[3])

    return


def find_rest(infos):
    for line in open("../data/lawyers0/" + infos[4].strip()):
        infos[6] = line.split('\t')[2].strip()
        infos[7] = line.split('\t')[3].strip()
        return


f = open("../data/all_offices_dec25.csv")

for line in f.readlines():
    infos = line.split(',')
    # no id!
    if not infos[4].strip():
        # find all lawyers
        find_id(infos)

    if not infos[6].strip() and infos[4].strip() != ".":
        find_rest(infos)
    
    print(infos[0] + "," + infos[1] + "," + infos[2] + "," + infos[3] + "," + infos[4] + "," + infos[5] + "," + infos[6] + "," + infos[7].strip())
