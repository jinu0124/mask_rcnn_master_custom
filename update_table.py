import os
import sys
import random
import time
import numpy as np
import json
import math
from datetime import datetime # 현재시간을 위해서
import pymysql
import parse_json
import time
# Maria DB에 테이블생성
# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
# labeling하여 만들어진 json 파일에 대해서 테이블에 정보 저장

sys.path.append(ROOT_DIR)  # To find local version of the library

#----------------------DB 연결하기
con = pymysql.connect(host = "localhost", user="root", password="1103", db = "road", charset='utf8')
cursor = con.cursor() # mysql을 조작할 커서

now = datetime.now()# 현재시간 받기
year, month, day, hour, minute, sec = now.year, now.month, now.day, now.hour, now.minute, now.second
#print(year, month, day, hour, minute)

number_of_files = len(parse_json.file_name_list)
labeling_whether = parse_json.whether_training
filename = parse_json.filename
size = parse_json.size
region_attributes = parse_json.region_attributes
regions_number = parse_json.regions_num_list
shape = parse_json.shape
train_val = parse_json.sel

filename_list = list()
for i in range(len(filename)):
    filename_list.append(i)

sub_filename = list()
sub_regions_number = list()
# sub_labeling 테이블에 들어갈 상세 정보(filename, regions, shape 정보를 매칭해서 한번에 넣기위해 list를 만들어줌), list 가공
for i in range (len(filename)):
    for j in range (len(regions_number[i])):
        sub_filename.append(filename[i])
        regions_number[i][j] = int(regions_number[i][j]) + 1 # 0부터 시작이 아닌 1부터 시작
        sub_regions_number.append(regions_number[i][j])
#print("file_ :",sub_filename)
#print("sub :",sub_regions_number)

print("labeling whether :", labeling_whether)
print("filename :", filename)
print("size :", size)
print("regions_attribute :", region_attributes, number_of_files)
print("regions_number :", regions_number)
print("shape :", shape)
print("train_val:", train_val)

dupl_filename = list()
dupl_number = list()
separated_num = list()

if train_val == "train":
    dupl_filenameQ = "select file_name from labeling where train_val = 'train'"
else:
    dupl_filenameQ = "select file_name from labeling where train_val = 'val'"

cursor.execute(dupl_filenameQ)
dupl_filename.append(cursor.fetchall())# Query로 요청한 값 받기

#print(dupl_filename[0][0][0])
#print(dupl_filename[0][1][0])
#print(len(filename), filename[0])

for i in range(len(filename)):
    for j in range(len(dupl_filename[0])):
        #print(filename[i], dupl_filename[0][j][0])
        if filename[i] == dupl_filename[0][j][0]:
            dupl_number.append(i) # dupl_number 리스트에 겹치는 번호들만 담음
            #print("yes")

print(dupl_number)
print("file_name_list", filename_list)

s = set(dupl_number)
separated_num = [x for x in filename_list if x not in s] # 리스트를 집합으로 바꾸어서 집합연산으로 빼기연산 수행 -> 중복 제거
print(separated_num) # 분리된 list number -> 현재 DB에 저장되어있지 않은 레코드

a = 0
b = 0
# SQL Query
insert_query_label = "insert into labeling(file_name, file_size, labeling_whether, train_val) values(%s, %s, %s, %s)"
insert_query_time = "insert into time(file_name, year, month, day, hour, minute, sec) values(%s, %s, %s, %s, %s, %s, %s)"
insert_query_sub = "insert into sub_labeling(file_name, regions_number, shape, region_attributes) values(%s, %s, %s, %s)"
for k in range(len(separated_num)):
    print(separated_num[k])

print(separated_num)
print(regions_number)
print(len(regions_number))
#zip = zip(regions_number, region_attributes)
#print(zip)
print(region_attributes)
print(len(region_attributes))
print(sub_regions_number)
#time.sleep(10)


r = 0
p = 0
pp = 0
for i in range(len(separated_num)): # separated num 분리되어 기존 DB에 없던 값들만 새로 넣어주기
    cursor.execute(insert_query_label, (filename[separated_num[i]], size[separated_num[i]], labeling_whether, train_val)) # labeling table에 새로운 data 삽입
    cursor.execute(insert_query_time, (filename[separated_num[i]], year, month, day, hour, minute, sec))# time table에 새로운 data 삽입
    print(len(regions_number[i]))
    #k = len(regions_number[i])
    #pp = p + k
    '''
    for j in range(len(regions_number[i])):
        #k = k - 1
        cursor.execute(insert_query_sub, (filename[separated_num[i]], regions_number[separated_num[i]][j], shape[r], region_attributes[r]))
        #[len(regions_number[i])] 중복되는 것 방지해서 DB에 넣기
        #print("p :", p, "k", k, "p + k :", p+k, "pp :", pp)
        r = r + 1
    '''
    #p = pp
    a = a + 1

if a == len(separated_num): # Query 문이 성공적으로 삽입 되었을 때 출력
    print("INSERT Query Success")
    con.commit()
    con.close()
else:
    print("INSERT Query Failed")

