#!/usr/bin/python3

import csv
import glob

import string
import random

import sys
sys.path.append('../classes')
from lawnbLawyer import Lawyer

def find_founders(office_name, founding_year, founders):

    if founding_year == '.':
        return


    files = glob.glob("../data/lawyers/P*")

    for file_to_read in files:
        f = open(file_to_read, 'r')
    
        lines = f.readlines()
        f.close()

        for line in lines:
            if office_name in line:
                rows = line.split('\t')
                if len(rows) > 9:
                    year = rows[9].replace("\n","")
                    if year is not '.':
                        if int(year) == int(founding_year):
                            founders.append(lines[0].split('\t')[1])
    return


def get_founding_year(office_name):
    year_file = open("../data/offices/founding_years.txt")
    ret = str('.')
    for line in year_file.readlines():
        if office_name in line:
            ret =  line.split('\t')[1].replace("\n","")

    year_file.close()
    return ret

def is_representative(career):
    if "대표" in career:
        return "1"
    else:
        return "0"

def get_office_id(career, c_name, c_sid):
    if "판사" in career:
        return '9999'
    elif "검사" in career:
        return '99999'
    elif c_name in career:
        return c_sid
    else:
        return '.'

def is_open_member(career, st_year, office_name):
    if office_name in career:
        founding_year = get_founding_year(office_name)
        if founding_year != '.':
            if founding_year == st_year:
                return '1'
    return '0'




def print_founders(c_name, c_sid, f_year, loc_1, loc_2, f_sids):

    result_file = '../data/offices/' + c_sid
    fw = open(result_file, 'w', newline='')
    f_writer = csv.writer(fw, delimiter = '\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    if len(f_sids) == 0:
        f_writer.writerow([c_name, c_sid, f_year, loc_1, loc_2])
    else:
        for f_sid in f_sids:
            html_file = '../data/html/' + f_sid.rstrip()
            fr = open(html_file)
            text = fr.read()
            
            if "요청하신 페이지를 찾을 수 없습니다." in text:
                return
            
            lawyer = Lawyer()
            lawyer.create(text, f_sid)
            #write first row
            f_writer.writerow([c_name, c_sid, f_year, loc_1, loc_2, lawyer.name, lawyer.sid, is_representative(lawyer.get_career(f_year, c_name)), lawyer.get_career(f_year, c_name).strip(), lawyer.birth, lawyer.sex, lawyer.bar_exam, lawyer.bar_period, lawyer.lawyer_exam, lawyer.major, lawyer.staple, lawyer.st_years[0], lawyer.ed_years[0], lawyer.highs[0], lawyer.univs[0], lawyer.grads[0], lawyer.careers[0], get_office_id(lawyer.careers[0], c_name, c_sid)])
            # write rows
            for i in range(1, len(lawyer.grads)):
                f_writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', lawyer.st_years[i], lawyer.ed_years[i], lawyer.highs[i], lawyer.univs[i], lawyer.grads[i], lawyer.careers[i], get_office_id(lawyer.careers[i], c_name, c_sid)])
 
            
            fr.close()
 


    fw.close()


def get_and_print_founders(company_and_sid, founding_year, locations):
    assert(len(company_and_sid) == 2)
    c_sid = company_and_sid[1].rstrip()
    company_name = company_and_sid[0].rstrip()

    founder_sids= []
    find_founders(company_name, founding_year, founder_sids)

    print_founders(company_name, c_sid, founding_year, locations[0], locations[1], founder_sids)

    
    
    

###########################################################
#                         main                            #
###########################################################

f = open("../data/region_list.csv")

while True:
    line = f.readline()
    if not line: break

    words = line.split()
    print(words)

    file_name = '../data/offices/' + words[0] + '_' + words[1]
    f_sid = open(file_name)

    company_sids = f_sid.readlines()
    for it in company_sids:
        company_and_sid = it.split(',')

        founding_year = get_founding_year(company_and_sid[0].strip())

        get_and_print_founders(company_and_sid, founding_year, words)


    f_sid.close()
f.close()


