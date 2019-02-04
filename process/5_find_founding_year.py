#!/usr/bin/python3

import glob


def add_space_to_careers(career):
    return career.replace("법무법인", " 법무법인 ").replace("법률사무소", " 법률사무소 ").replace("(", " (").replace(")", " ) ")


def find_year(office_name):

    files = glob.glob("../data/lawyers/P*")

    years = []

    for file_to_read in files:
        f = open(file_to_read, 'r')
    
        lines = f.readlines()
        f.close()

        for line in lines:
            if " "+ office_name.replace("법무법인", "").strip() + " " in " " + add_space_to_careers(line.split('\t')[17].strip()) + " ":
                if len(line.split('\t')) > 10:
                    year = line.split('\t')[9]
                if year == '.': break
                years.append(int(year))

    if len(years) == 0:
        return "."

    return min(years)
        

###########################################################
#                         main                            #
###########################################################


f = open("../data/FirmList_1643.csv")


while True:
    line = f.readline()
    if not line: break

    words = line.split(',')
    if 'before' in words[1]:
        print(words[0].strip() + ',' + str(find_year(words[0].strip())) + ','+  words[2].strip() + ',' + words[3].strip() + ',' + words[4].strip())
    else:
        print(words[0].strip() + ',' + words[1].strip() + ',' +  words[2].strip() + ',' + words[3].strip() + ',' + words[4].strip())


