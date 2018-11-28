#!/usr/bin/python3

import requests

url = "http://lawnb.com/AjaxInfo/ContentList"

for i in range(230, 400, 10):
    payload = {'sPage': '1','sList': '1100','sCode': 'P001','sType': '1', 'sSubType': '1', 'sSort':'0','sSortChk_2': '0','sWord':'','sCat1': i,'sCat2': '00'}
    res = requests.post(url, data=payload)
    print(res.text)

