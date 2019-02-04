#!/usr/bin/python3


firm_file = open("firmlist_1643.csv")

def get_region(firm_name):
    f = open("../data/region_list.csv")
    while True:
        line = f.readline()
        if not line: break
    
        words = line.split()
        file_name = '../data/offices/' + words[0] + '_' + words[1]
        f_sid = open(file_name)
        for firmList in f_sid.readlines():
            if firm_name in firmList.split(',')[0]:
                f_sid.close()
                f.close()
                return words[0].strip() + "," + words[1].strip()
    
    
        
        f_sid.close()
    f.close()
    return ".,."





for line in firm_file.readlines():
    if line.split(',')[4].strip():
        print(line.strip())
    else:
        print(line.strip() + "," + get_region(line.split(',')[0]))
