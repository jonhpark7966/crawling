#!/usr/bin/python3

import requests
import csv

import string
import random

import sys
sys.path.append('../classes')
from lawnbLawyer import Lawyer

###########################################################
#                         main                            #
###########################################################


file_name = '../data/members/lawyers.txt'
f_sid = open(file_name)


lawyer_sids = f_sid.readlines()
for sid in lawyer_sids:
   print(sid.rstrip())
   
   result_file = '../data/lawyers/' + sid.rstrip()
   fw = open(result_file, 'w', newline='')
   f_writer = csv.writer(fw, delimiter = '\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)


   html_file = '../data/html/' + sid.rstrip()
   fr = open(html_file)
   text = fr.read()

   if "요청하신 페이지를 찾을 수 없습니다." in text:
       break

   lawyer = Lawyer()
   lawyer.create(text, sid.rstrip())
   lawyer.write(f_writer)

   fw.close()
   fr.close()


f_sid.close()
