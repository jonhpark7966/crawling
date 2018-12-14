from bs4 import BeautifulSoup
import re
import csv
import random
import string
import glob

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def dot_if_empty(text):
    if len(text) == 0:
        return '.'
    else:
        return text

def get_high_id(text):
    f = open("../data/lawyers/high_list.txt")
    i = 0
    for line in f.readlines():
        if line.strip() in text:
            return 'h' + str(i)
        i = i + 1
    f.close()
    return '.'

def get_univ_id(text):
    f = open("../data/lawyers/university_list.txt")
    for line in f.readlines():
        if line.split("\t")[1].strip() in text:
            return 'u' + line.split('\t')[0].strip()
    f.close()
    return '.'

def get_grad_id(text):
    f = open("../data/lawyers/graduate_list.txt")
    for line in f.readlines():
        if line.split("\t")[1].strip() in text:
            return 'g' + line.split('\t')[0].strip()
    f.close()
    return '.'


def get_company_id(text):
    f = open("../data/offices/all.txt")
    for line in f.readlines():
        if line.split(',')[0].strip() in text:
            return line.split(',')[1].strip()
    f.close()
    return '.'





class Lawyer:
    def create(self, html_text, lawyer_sid):

        self.sid = lawyer_sid
    
        soup = BeautifulSoup(html_text, 'html.parser')

        #birth, sex, bar exam, bar period, lawyer exam
        infos_first = soup.select('#lawyer_info_tit > span > em')
        self.birth = '.'
        self.sex = '.'
        self.bar_exam = '.'
        self.bar_period = '.'
        self.lawyer_exam = '.'
        if len(infos_first) > 0:
            for info in infos_first:
                if "년생" in info.text:
                    self.birth = re.split('년', info.text.strip())[0]
                if "남자" in info.text or "여자" in info.text:
                    self.sex = info.text.strip()
                if "사법시험" in info.text:
                    self.bar_exam = re.split(' |회',info.text.strip())[1]
                if "연수원" in info.text:
                    self.bar_period = re.split('원|기',info.text.strip())[1]
                if "변호사시험" in info.text:
                    self.lawyer_exam = re.split(' |회',info.text.strip())[1]
        ####################################################
    
        #major(전문), staple(주요)
        self.major = '.'
        self.staple = '.'
        lawyer_info_divs = soup.select('div.lawyer_info > span')
        assert(len(lawyer_info_divs) > 0) # check layer_info _default exist!
        for content in lawyer_info_divs:
            if "주요업무분야" in content.text:
                self.staple = re.split(':', content.text.strip())[1].strip().replace('"','')
            if "전문분야" in content.text:
                self.major = re.split(':', content.text.strip())[1].strip().replace('"','')
        #######################################################
    
    
        #name 
        self.name = re.split( ',|\(| ', str(soup.find('title')))[3]
        #######################################################
    
    
        #company, job, position, address
        self.company = '.'
        self.job = '.'
        self.position = '.'
        self.address = '.'
        lawyer_info_divs = soup.select('div.lawyer_info')
        assert(len(lawyer_info_divs) > 0)
        for content in lawyer_info_divs:
            if "현직 정보" in content.text:
                for cell in content.select('ul > li'):
                    #company
                    if "소속" in cell.select('span')[0].text:
                        if len(cell.contents)>1:
                            self.company = cell.contents[1].strip()
                    #job & position
                    if "직업/직책" in cell.text:
                        if len(cell.contents)>1:
                            j_and_p = re.split('/',cell.contents[1])
                            if len(j_and_p) > 0:
                                self.job = j_and_p[0].strip()
                            if len(j_and_p) > 1:
                                self.position = j_and_p[1].strip()
                    #address
                    if "주소" in cell.text:
                        if len(cell.contents)>1:
                            self.address = cell.contents[1].strip()
                break
        #######################################################
    
        #to make school & career togather
        self.st_years = []
        self.ed_years = []
        self.careers = []
    
        #school infos
        self.highs = []
        self.univs = []
        self.grads = [] 
        sch_info = soup.select_one('#school_info > ul.school')
        if sch_info is not None:
            sch_i = 3
            schs = sch_info.select('li')
            while sch_i < len(schs):
                #high school
                if "고등학교" in schs[sch_i].text:
                    self.highs.append(schs[sch_i].text.strip().replace("\n","").strip())
                    self.st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                    self.ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                    self.univs.append('.')
                    self.grads.append('.')
                    self.careers.append('.')
                #university
                if "대학교" in schs[sch_i].text and "대학원" not in schs[sch_i].text and "LL.M" not in schs[sch_i].text and "석사" not in schs[sch_i].text and "수료" not in schs[sch_i].text and "박사" not in schs[sch_i].text and "Law School" not in schs[sch_i].text and "School of Law" not in schs[sch_i].text:
                    self.univs.append(schs[sch_i].text.strip().replace("  ","").replace("\r","").replace("\n","").split('/')[0].split('대학')[0].strip())
                    self.st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                    self.ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                    self.highs.append('.')
                    self.grads.append('.')
                    self.careers.append('.')
                #graduate school
                if "대학원" in schs[sch_i].text or "LL.M" in schs[sch_i].text or "석사" in schs[sch_i].text or "수료" in schs[sch_i].text or "박사" in schs[sch_i].text or "Law School" in schs[sch_i].text or "School of Law" in schs[sch_i].text:
                    self.grads.append(schs[sch_i].text.strip().replace("  ","").replace("\r","").replace("\n","").replace("Law School", "/").replace("School of Law","/").replace("LL", "/").split('/')[0].split('대학')[0].strip())
                    self.st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                    self.ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                    self.highs.append('.')
                    self.univs.append('.')
                    self.careers.append('.')
    
                sch_i += 3
        #######################################################
    
    
        #career infos
        sch_info = soup.select_one('#career_info > ul.school')
        if sch_info is not None:
            sch_i = 3
            schs = sch_info.select('li')
            while sch_i < len(schs):
    
                #career
                self.careers.append(schs[sch_i].text.strip().replace("  ","").replace("\n","").strip())
                self.st_years.append(dot_if_empty(schs[sch_i+1].text.strip().split('.')[0]))
                self.ed_years.append(dot_if_empty(schs[sch_i+2].text.strip().split('.')[0]))
                self.highs.append('.')
                self.univs.append('.')
                self.grads.append('.')
    
                sch_i += 3
        #######################################################
    
    
    
        # to make empty string for first row
        if len(self.highs) == 0:
            self.highs.append('.')
            self.univs.append('.')
            self.grads.append('.')
            self.careers.append('.')
            self.st_years.append('.')
            self.ed_years.append('.')
        ##################################

    def write(self, csv_writer):
        # write first row
        csv_writer.writerow([self.name, self.sid, self.birth, self.sex, self.bar_exam, self.bar_period, self.lawyer_exam, self.major, self.staple, self.st_years[0], self.ed_years[0], self.highs[0], get_high_id(self.highs[0]), self.univs[0], get_univ_id(self.univs[0]), self.grads[0], get_grad_id(self.grads[0]), self.careers[0], get_company_id(self.careers[0])])
        # write rows
        for i in range(1, len(self.grads)):
            csv_writer.writerow(['', '', '', '', '', '', '', '', '', self.st_years[i], self.ed_years[i], self.highs[i],  get_high_id(self.highs[i]), self.univs[i], get_univ_id(self.univs[i]), self.grads[i], get_grad_id(self.grads[i]), self.careers[i], get_company_id(self.careers[i])])

    def get_career(self, year, c_name):
        i = 0
        for st_year in self.st_years:
            if st_year != '.':
                if int(st_year) == int(year):
                    if c_name in self.careers[i]:
                        return self.careers[i]
            i = i +1
        return '.'

    

