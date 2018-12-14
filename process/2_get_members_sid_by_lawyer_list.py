#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re

url = "http://lawnb.com/AjaxInfo/ContentLawyerList"

write_file_name = '../data/members/lawyers_text.txt'
fw = open(write_file_name, 'w', newline='')

for i in range(1910,2000): 

    
    payload = {'sPage': '1','sList': '1500','sCode': 'P000','sType': '1',  'sSort':'0', 'sSortChk_1':'0', 'sSortChk_2':'0','sJobCode':'00', 'sTestCode':'00', 'sBirthS': str(i), 'sBirthE': str(i), 'cJobCode': '00', 'cTestCode': '00', 'cBirthS': str(i), 'csBirthE': str(i)}
    res = requests.post(url, data=payload)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    #contents html div that includes lawyer name and sid
    contents = soup.select('div.co_searchContent > h3 > a')
    
    print(str(i) + ',' + str(len(contents)))
    for content in contents:
        cnt_str = str(content)
        fw.write(cnt_str.split('"')[3].split('?')[1].split('=')[1] + '\n')
    

fw.close()
