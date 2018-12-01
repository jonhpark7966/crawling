#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re


url = "http://lawnb.com/AjaxInfo/ContentList"

f = open("../data/region_list.csv")

while True:
    line = f.readline()
    if not line: break

    words = line.split()

    file_name = '../data/offices/' + words[0] + '_' + words[1]
    fw = open(file_name, 'w', newline='')

    payload = {'sPage': '1','sList': '1100','sCode': 'P001','sType': '1', 'sSubType': '1', 'sSort':'0','sSortChk_2': '0','sWord':'','sCat1': words[2],'sCat2': words[3]}
    res = requests.post(url, data=payload)
    soup = BeautifulSoup(res.text, 'html.parser')

    firms_info = soup.select('div.co_searchContent')
    # for each firm
    for firm_info in firms_info:
        members = firm_info.select('div.firm_etc > div.btn-group > span')
        assert(members[1].text == '구성원')
        sid = re.split("['?=]", str(members[1]))[5]
        fw.write(firm_info.select('div.firm_name')[0].text + ',' + sid + '\n')
    fw.close()
f.close()
