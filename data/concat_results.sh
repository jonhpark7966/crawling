#!/bin/bash

for rgn in 서울시 경기도 강원도 충남 충북 경상북도 전라북도 경상남도 전라남도 제주도 인천시 울산시 부산시 광주시 대전시 대구시 기타
do
	cat results/$rgn* > results_by_rgn/$rgn.txt
done
