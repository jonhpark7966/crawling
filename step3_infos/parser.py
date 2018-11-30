#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re
import csv

csv_f = open('tab_seperated_test.txt', 'w', newline='')
f_writer = csv.writer(csv_f, delimiter = '\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#TODO: first row. for indexing!!!!
#f_writer.writerow([]);

f = open("./info_html.txt")
a_html_doc = ''
while True:
    line = f.readline()
    if not line: break
   
    a_html_doc = a_html_doc + line.rstrip()

    if line.rstrip() == "</html>":
        soup = BeautifulSoup(a_html_doc, 'html.parser')


        #birth, sex, bar exam, bar period, lawyer exam
        ##################################################
        infos1 = soup.select('#lawyer_info_tit > span > em')
        birth = ''
        sex = ''
        bar_exam = ''
        bar_period = ''
        lawyer_exam = ''
        if len(infos1) > 0:
            for info in infos1:
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
        ######################################################
        major = ''
        staple = ''
        lawyer_info_divs = soup.select('div.lawyer_info > span')
        assert(len(lawyer_info_divs) > 0) # check layer_info _default exist!
        for content in lawyer_info_divs:
            if "주요업무분야" in content.text:
                staple = re.split(':', content.text.strip())[1].strip().replace('"','')
            if "전문분야" in content.text:
                major = re.split(':', content.text.strip())[1].strip().replace('"','')
        #######################################################


        #name 
        ######################################################
        name = re.split( ',|\(| ', str(soup.find('title')))[3]
        # assertion! name should be exist!
        #######################################################


        #company, job, position, address
        #######################################################
        company = ''
        job = ''
        position = ''
        address = ''
        lawyer_info_divs = soup.select('div.lawyer_info')
        assert(len(lawyer_info_divs) > 0)
        for content in lawyer_info_divs:
            if "현직 정보" in content.text:
                for cell in content.select('ul > li'):
                    #company
                    if "소속" in cell.text:
                        if len(cell.contents)>1:
                            company = cell.contents[1].strip()
                    #job & position
                    if "직업/직책" in cell.text:
                        if len(cell.contents)>1:
                            job = re.split('/',cell.contents[1])[0].strip()
                            position = re.split('/',cell.contents[1])[1].strip()
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
        #######################################################
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
                    st_years.append(schs[sch_i+1].text.strip())
                    ed_years.append(schs[sch_i+2].text.strip())
                    univs.append('')
                    grads.append('')
                    careers.append('')
                #university
                if "대학교" in schs[sch_i].text and "대학원" not in schs[sch_i].text and "LL.M" not in schs[sch_i].text and "석사" not in schs[sch_i].text and "수료" not in schs[sch_i].text and "박사" not in schs[sch_i].text and "Law School" not in schs[sch_i].text and "School of Law" not in schs[sch_i].text:
                    univs.append(schs[sch_i].text.strip().replace("  ",""))
                    st_years.append(schs[sch_i+1].text.strip())
                    ed_years.append(schs[sch_i+2].text.strip())
                    highs.append('')
                    grads.append('')
                    careers.append('')
                #graduate school
                if "대학원" in schs[sch_i].text or "LL.M" in schs[sch_i].text or "석사" in schs[sch_i].text or "수료" in schs[sch_i].text or "박사" in schs[sch_i].text or "Law School" in schs[sch_i].text or "School of Law" in schs[sch_i].text:
                    grads.append(schs[sch_i].text.strip().replace("  ",""))
                    st_years.append(schs[sch_i+1].text.strip())
                    ed_years.append(schs[sch_i+2].text.strip())
                    highs.append('')
                    univs.append('')
                    careers.append('')

                sch_i += 3
        #######################################################


        #career infos
        #######################################################
        sch_info = soup.select_one('#career_info > ul.school')
        if sch_info is not None:
            sch_i = 3
            schs = sch_info.select('li')
            while sch_i < len(schs):

                #career
                careers.append(schs[sch_i].text.strip().replace("  ",""))
                st_years.append(schs[sch_i+1].text.strip())
                ed_years.append(schs[sch_i+2].text.strip())
                highs.append('')
                univs.append('')
                grads.append('')

                sch_i += 3
        #######################################################



        # to make empty string for first row
        #################################
        if len(highs) == 0:
            highs.append('')
            univs.append('')
            grads.append('')
            careers.append('')
            st_years.append('')
            ed_years.append('')
        ##################################

        # write first row
        f_writer.writerow([company, name, birth, sex, bar_exam, bar_period, lawyer_exam, major, staple, company, job, position, st_years[0], ed_years[0], highs[0], univs[0], grads[0], careers[0], address])
        # write rows
        for i in range(1, len(grads)):
            f_writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', st_years[i], ed_years[i], highs[i], univs[i], grads[i], careers[i], ''])

        a_html_doc = ''

f.close()
csv.close()
