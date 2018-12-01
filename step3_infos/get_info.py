#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re


f = open("../step2_lawyers/lawyers.txt")
while True:
    sid = f.readline()
    if not sid: break

    url = "http://lawnb.com/Info/ContentView?sid=" + sid.rstrip()
    #print(url)

    session_ck = {'ASP.NET_SessionId':'bwytqqduugzrg43o2q0sgjj1'}
    res = requests.get(url, cookies=session_ck)
    print(res.text)

    #contents html div that includes lawyer name and sid
    #contents = soup.find_all('div', {'class': 'co_searchContent'})

    #for content in contents:
    #    cnt_str = str(content)
    #    print(cnt_str.split('"')[5])

f.close()

#soup = BeautifulSoup(res.text, 'html.parser')
#
##name
#name_tag = soup.find('h2')
#print(re.split( ', |>', str(name_tag))[1])


#company, job, position
