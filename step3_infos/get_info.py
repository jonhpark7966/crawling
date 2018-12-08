#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re
import csv

import string
import random

import sys

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def dot_if_empty(text):
    if len(text) == 0:
        return '.'
    else:
        return text
  

def parser(html_text, csv_writer):
    soup = BeautifulSoup(html_text, 'html.parser')

    #birth, sex, bar exam, bar period, lawyer exam
    infos_first = soup.select('#lawyer_info_tit > span > em')
    birth = '.'
    sex = '.'
    bar_exam = '.'
    bar_period = '.'
    lawyer_exam = '.'
    if len(infos_first) > 0:
        for info in infos_first:
            if "년생" in info.text:
                birth = re.split('년', info.text.strip())[0]
            if "남자" in info.text or "여자" in info.text:
                sex = info.text.strip()
            if "사법시험" in info.text:
                bar_exam = re.split(' |회',info.text.strip())[1]
            if "연수원" in info.text:
                bar_period = re.split('원|기',info.text.strip())[1]
            if "변호사시험" in info.text:
                lawyer_exam = re.split(' |회',info.text.strip())[1]
    ####################################################

    #major(전문), staple(주요)
    major = '.'
    staple = '.'
    lawyer_info_divs = soup.select('div.lawyer_info > span')
    assert(len(lawyer_info_divs) > 0) # check layer_info _default exist!
    for content in lawyer_info_divs:
        if "주요업무분야" in content.text:
            staple = re.split(':', content.text.strip())[1].strip().replace('"','')
        if "전문분야" in content.text:
            major = re.split(':', content.text.strip())[1].strip().replace('"','')
    #######################################################


    #name 
    name = re.split( ',|\(| ', str(soup.find('title')))[3]
    #######################################################


    #company, job, position, address
    company = '.'
    job = '.'
    position = '.'
    address = '.'
    lawyer_info_divs = soup.select('div.lawyer_info')
    assert(len(lawyer_info_divs) > 0)
    for content in lawyer_info_divs:
        if "현직 정보" in content.text:
            for cell in content.select('ul > li'):
                #company
                if "소속" in cell.select('span')[0].text:
                    if len(cell.contents)>1:
                        company = cell.contents[1].strip()
                #job & position
                if "직업/직책" in cell.text:
                    if len(cell.contents)>1:
                        j_and_p = re.split('/',cell.contents[1])
                        if len(j_and_p) > 0:
                            job = j_and_p[0].strip()
                        if len(j_and_p) > 1:
                            position = j_and_p[1].strip()
                #address
                if "주소" in cell.text:
                    if len(cell.contents)>1:
                        address = cell.contents[1].strip()
            break
    #######################################################

    #to make school & career togather
    st_years = []
    ed_years = []
    careers = []

    #school infos
    highs = []
    univs = []
    grads = [] 
    sch_info = soup.select_one('#school_info > ul.school')
    if sch_info is not None:
        sch_i = 3
        schs = sch_info.select('li')
        while sch_i < len(schs):
            #high school
            if "고등학교" in schs[sch_i].text:
                highs.append(schs[sch_i].text.strip())
                st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                univs.append('.')
                grads.append('.')
                careers.append('.')
            #university
            if "대학교" in schs[sch_i].text and "대학원" not in schs[sch_i].text and "LL.M" not in schs[sch_i].text and "석사" not in schs[sch_i].text and "수료" not in schs[sch_i].text and "박사" not in schs[sch_i].text and "Law School" not in schs[sch_i].text and "School of Law" not in schs[sch_i].text:
                univs.append(schs[sch_i].text.strip().replace("  ","").replace("\r","").replace("\n",""))
                st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                highs.append('.')
                grads.append('.')
                careers.append('.')
            #graduate school
            if "대학원" in schs[sch_i].text or "LL.M" in schs[sch_i].text or "석사" in schs[sch_i].text or "수료" in schs[sch_i].text or "박사" in schs[sch_i].text or "Law School" in schs[sch_i].text or "School of Law" in schs[sch_i].text:
                grads.append(schs[sch_i].text.strip().replace("  ","").replace("\r","").replace("\n",""))
                st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                highs.append('.')
                univs.append('.')
                careers.append('.')

            sch_i += 3
    #######################################################


    #career infos
    sch_info = soup.select_one('#career_info > ul.school')
    if sch_info is not None:
        sch_i = 3
        schs = sch_info.select('li')
        while sch_i < len(schs):

            #career
            careers.append(schs[sch_i].text.strip().replace("  ",""))
            st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
            ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
            highs.append('.')
            univs.append('.')
            grads.append('.')

            sch_i += 3
    #######################################################



    # to make empty string for first row
    if len(highs) == 0:
        highs.append('.')
        univs.append('.')
        grads.append('.')
        careers.append('.')
        st_years.append('.')
        ed_years.append('.')
    ##################################

    # write first row
    csv_writer.writerow([id_generator(), id_generator(), words[0], words[1], company, name, birth, sex, bar_exam, bar_period, lawyer_exam, major, staple, company, job, position, st_years[0], ed_years[0], highs[0], univs[0], grads[0], careers[0], address])
    # write rows
    for i in range(1, len(grads)):
        csv_writer.writerow(['', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', st_years[i], ed_years[i], highs[i], univs[i], grads[i], careers[i], ''])

    return;


###########################################################
#                         main                            #
###########################################################

if len(sys.argv) != 2:
    print("usage: ./get_info.py $Session Coockie")


f = open("../data/region_list.csv")

while True:
    line = f.readline()
    if not line: break

    words = line.split()
    print(words)

    file_name = '../data/members/' + words[0] + '_' + words[1]
    f_sid = open(file_name)

    write_file_name = '../data/results/' + words[0] + '_' + words[1]
    fw = open(write_file_name, 'w', newline='\n')
    f_writer = csv.writer(fw, delimiter = '\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    lawyers = f_sid.readlines()
    for lawyer in lawyers:
        company_sid = lawyer.split(',')

        if len(company_sid) == 2:
            sid = company_sid[1]
            url = "http://lawnb.com/Info/ContentView?sid=" + sid.rstrip()

            session_ck = {'ASP.NET_SessionId':str(sys.argv[1])}
            res = requests.get(url, cookies=session_ck)

            parser(res.text, f_writer)
    

        elif len(company_sid) == 1:#NO LAWYER
            f_writer.writerow([id_generator(), '', words[0], words[1], company_sid[0].strip(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

    fw.close()
    f_sid.close()
            


f.close()


