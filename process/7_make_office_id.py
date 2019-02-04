#!/usr/bin/python3

import csv
import glob

import string
import random

import sys
    

###########################################################
#                         main                            #
###########################################################

f = open("../data/offices/all.txt")

while True:
    line = f.readline()
    if not line: break

    words = line.split(',')

    if not words[1].startswith("P"):
        words[1] = "N" + str(random.randrange(1000000000, 9999999999))


    print(words[0].strip() + "," + words[1].strip())


f.close()


