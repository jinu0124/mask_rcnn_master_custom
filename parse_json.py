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

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
# json파일 RDBMS에 저장하고 활용할 수 있도록 파싱하기

sys.path.append(ROOT_DIR)  # To find local version of the library

sel = "train"# train or val

JSON1 = os.path.join(ROOT_DIR, "samples\\load\\")
JSON = os.path.join(JSON1, "dataset\\")
print(JSON)

assert sel in ["train", "val"]
if sel == "train":
    JSON = os.path.join(JSON, "train\\")
    preparse = json.load(open(os.path.join(JSON, "via_region_data.json"))) #preparse라는 이름으로 json파일을 읽어들임
else:
    JSON = os.path.join(JSON, "val\\")
    preparse = json.load(open(os.path.join(JSON, "via_region_data.json")))

indent = json.dumps(preparse, indent="\t")# indent 에 이쁘게 들여쓰기 된 json파일 넣기
print("read : ", preparse, "\n", indent)

file_name = preparse.keys()# 최상단 키값 받아오기, Dictionary 형태로 받아오게됨 {[' ',' ',' ',' ']}
#print(file_name)
file_name_list = list(file_name) # list 형태로 변환
print("Number of files :", len(file_name_list))

filename = list()
size = list()
region_attributes = list()
regions_num_list = list()
shape = list()

for i in range (len(file_name_list)): # 읽은 json 파일의 key값의 갯수 만큼 LOOP 돌며 값 추출, list로 저장 나중에 Maria DB로 저장하기
    size.append(preparse[file_name_list[i]]["size"])
    filename.append(preparse[file_name_list[i]]["filename"])
    for j in range (len(preparse[file_name_list[i]]["regions"])):
        stt = str(j)
        region_attributes.append(preparse[file_name_list[i]]["regions"][stt]["region_attributes"]["name"])
    regions_num = (preparse[file_name_list[i]]["regions"])
    regions_num = list(regions_num)# 위 for문에서 regions_num = preparse~~["regions"]로부터 모든 regions 하위 키값들을 추출(Dictionary형태로) 후 list형태로 변환
    regions_num_list.append(regions_num)# 0,1,2,3.. 과 같이 번호만 남으므로 regions_num_list로 값을 append
    for j in range (len(regions_num_list[i])): # regions의 key 갯수만큼 가져옴 name : polygon
        st = str(j) # String 형으로 변환해야 json 파일로 부터 읽어올때 에러 발생 X
        shape.append(preparse[file_name_list[i]]["regions"][st]["shape_attributes"]["name"])
    #shape_attributes.append(preparse[file_name_list[i]]["regions"])

print(len(region_attributes))

whether_training = 1 # 1이면 트레이닝 이미 진행함 / 0이면 트레이닝 이전
now = datetime.now()# 현재시간 받기
year, month, day, hour, minute, sec = now.year, now.month, now.day, now.hour, now.minute, now.second
#print(year, month, day, hour, minute)
