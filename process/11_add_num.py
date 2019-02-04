#!/usr/bin/python3
# -*- coding: utf-8 -*-


f = open("../data/all_offices_dec26.csv")

cnt = 0
name = ""

for line in f.readlines():
    infos = line.split(',')

    if not name:
        name = infos[0].strip() 

    if infos[0].strip() != name:
        for i in range(cnt):
            print(cnt)
        cnt = 0
        name = ""
   
    cnt = cnt + 1

for i in range(cnt):
    print(cnt)

