#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob

files = glob.glob("../data/lawyers_v2/P*")
for file_to_read in files:
    f = open(file_to_read)
    for line in f.readlines():
        st_year = line.split('\t')[9] 
        ed_year = line.split('\t')[10] 
        if st_year != "." and ed_year != ".":
            try:
                for i in range(int(st_year), int(ed_year)+1):
                    print(line.replace(st_year, str(i)).replace(ed_year,str(i)).strip())
            except:
                print(line.strip())
        else:
            print(line.strip())


