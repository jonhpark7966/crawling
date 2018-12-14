#!/usr/bin/python3

import glob

def find_year(office_name):

    files = glob.glob("../data/lawyers/P*")

    years = []

    for file_to_read in files:
        f = open(file_to_read, 'r')
    
        lines = f.readlines()
        f.close()


        for line in lines:
            if office_name in line:
                if len(line.split('\t')) < 10:
                    print(f)
                    print(line)
                year = line.split('\t')[9]
                if year == '.': break
                years.append(int(year))

    if len(years) == 0:
        return "."

    return min(years)
        

###########################################################
#                         main                            #
###########################################################


f = open("../data/foundyears.csv")


while True:
    line = f.readline()
    if not line: break

    words = line.split(',')
    if 'before' in words[1]:
        print(words[0].strip() + '\t' + str(find_year(words[0].strip())))
    else:
        print(words[0].strip() + '\t' + words[1].strip())

