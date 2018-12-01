#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re

url = "http://lawnb.com/AjaxInfo/ContentLawyerList"

f = open("../data/region_list.csv")

while True:
    line = f.readline()
    if not line: break

    words = line.split()
    print(words)

    file_name = '../data/offices/' + words[0] + '_' + words[1]
    f_sid = open(file_name)

    write_file_name = '../data/members/' + words[0] + '_' + words[1]
    fw = open(write_file_name, 'w', newline='')



    offices = f_sid.readlines()
    for office in offices: 

        sid = office.split(',')[1]
        
        payload = {'sPage': '1','sList': '10000','sCode': 'P000','sType': '1', 'sType5': sid, 'sSort':'1', 'sSortChk_1':'0', 'sSortChk_2':'0'}
        res = requests.post(url, data=payload)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        #contents html div that includes lawyer name and sid
        contents = soup.find_all('div', {'class': 'co_searchContent'})

        if len(contents) == 0 :
            fw.write(office.split(',')[0] + '\n')
        
        for content in contents:
            cnt_str = str(content)
            fw.write(office.split(',')[0] + ',' + cnt_str.split('"')[5].split('?')[1].split('=')[1]+'\n')

    
    f_sid.close()
    fw.close()

f.close()
