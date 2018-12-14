#!/usr/bin/python3

import requests
import csv

import string
import random

import sys
sys.path.append('../classes')
from lawnbLawyer import Lawyer

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

  


###########################################################
#                         main                            #
###########################################################

if len(sys.argv) != 2:
    print("usage: ./$binary $Session Coockie")


write_file_name = '../data/results/all_lawyers'
fw = open(write_file_name, 'w', newline='\n')
f_writer = csv.writer(fw, delimiter = '\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)




file_name = '../data/members/lawyers.txt'
f_sid = open(file_name)


lawyer_sids = f_sid.readlines()
for sid in lawyer_sids:

    print(sid)
    url = "http://lawnb.com/Info/ContentView?sid=" + sid.rstrip()

    session_ck = {'ASP.NET_SessionId':str(sys.argv[1])}
    res = requests.get(url, cookies=session_ck)

    
    html_file = '../data/html/' + sid.rstrip()
    fww = open(html_file, 'w', newline='')
    fww.write(res.text)
    fww.close()

f_sid.close()

fw.close()
