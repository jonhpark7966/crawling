#!/usr/bin/python3
# -*- coding: utf-8 -*-

f1 = open("../data/231.csv")
f2 = open("../data/founders.csv")


def in_results(line, results):
    for result in results:
        if line.split(',')[1] in result:
            return False
    return True


results = []

for line in f1.readlines():
    results.append(line)

for line in f2.readlines():
    if not in_results(line, results):
        results.append(line)


 
for line in results:
    print(line.strip())

