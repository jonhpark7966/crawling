#!/bin/bash

echo "STEP1 offices starts"
cd step1_offices
./get_office.py
cd ../

echo "STEP2 lawyers starts"
cd step2_lawyers
./get_members_sid.py
cd ../

echo "STEP3 infos starts"
cd step3_infos
./get_info.py bwytqqduugzrg43o2q0sgjj1
cd ../

cd data
./concat_results.sh
cd ../

echo "FINISH!"
