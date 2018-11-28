#!/bin/bash

./get_office_html.py | grep "구성원" | awk -F\' '{print $2}'
