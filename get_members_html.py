#!/usr/bin/python3

print("Author ': Jong Hyun Park")


from bs4 import BeautifulSoup

import requests

url = "http://lawnb.com/AjaxInfo/ContentLawyerList"

#for sid in 'P0011305901':
sid = 'P0011305901'
payload = {'sPage': '1','sList': '1','sCode': 'P000','sType': '1', 'sType5': 'P0011305901', 'sSort':'1', 'sSortChk_1':'0', 'sSortChk_2':'0'}
res = requests.post(url, data=payload)
print(res.text)

