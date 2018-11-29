#!/usr/bin/python3

print("Author : Jong Hyun Park")


from bs4 import BeautifulSoup
import requests
import re

url = "http://lawnb.com/AjaxInfo/ContentLawyerList"

f = open("../step1_offices/sids1.txt")
while True:
    sid = f.readline()

    payload = {'sPage': '1','sList': '10000','sCode': 'P000','sType': '1', 'sType5': sid, 'sSort':'1', 'sSortChk_1':'0', 'sSortChk_2':'0'}
    res = requests.post(url, data=payload)
    soup = BeautifulSoup(res.text, 'html.parser')

    #contents html div that includes lawyer name and sid
    contents = soup.find_all('div', {'class': 'co_searchContent'})

    for content in contents:
        cnt_str = str(content)
        print(cnt_str.split('"')[5])

    if not sid: break
f.close()
