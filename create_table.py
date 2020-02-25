import os
import sys
import random
import math
import re
import time
import numpy as np
import json
import math
from datetime import datetime # 현재시간을 위해서
import pymysql
# Maria DB에 테이블생성
# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
# json파일 RDBMS에 저장하고 활용할 수 있도록 파싱하기

sys.path.append(ROOT_DIR)  # To find local version of the library

#----------------------DB 연결하기
con = pymysql.connect(host = "localhost", user="root", password="1103", db = "road", charset='utf8')
cursor = con.cursor() # mysql을 조작할 커서

whether_training = 1 # 1이면 트레이닝 이미 진행함 / 0이면 트레이닝 이전
now = datetime.now()# 현재시간 받기
year, month, day, hour, minute, sec = now.year, now.month, now.day, now.hour, now.minute, now.second
#print(year, month, day, hour, minute)

# SQL Query
table_query1 = "Create table if not exists labeling(" \
              "file_name varchar(100)," \
              "file_size int check(file_size > 0)," \
               "labeling_whether int," \
               "train_val varchar(10)," \
               "primary key (file_name, train_val))" \

table_query2 = "Create table if not exists time(" \
               "file_name varchar(100)," \
               "year int check(year>=1970)," \
               "month int check(month>=0)," \
               "day int check(day>=0)," \
               "hour int check(hour>=0)," \
               "minute int check(minute>=0)," \
               "sec int check(sec>=0)," \
               "primary key (year, month, day, hour, minute, sec, file_name)," \
               "Foreign key (file_name) references labeling(file_name) on delete cascade on update cascade)"

table_query3 = "Create table if not exists sub_labeling(" \
               "file_name varchar(100)," \
               "regions_number int," \
               "shape varchar(20)," \
               "region_attributes varchar(50)," \
               "Foreign key (file_name) references labeling(file_name) on delete cascade on update cascade)"

cursor.execute(table_query1) # labeling 정보 테이블 생성
cursor.execute(table_query2) # labeling 파일에 대한 timestamp 테이블 생성
cursor.execute(table_query3) # labeling 정보 중 NF(정규화)에 따라서 분리(shape, regions_넘버링))
con.commit()
con.close()
