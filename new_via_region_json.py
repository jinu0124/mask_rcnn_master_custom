import os
import sys
import random
import math
import re
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import math
# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
#JSON 파일 합치기 via_region_data.json + via_region_data (2).json -> new_via_region_data.json

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library

sel = "train"# train or val

JSON1 = os.path.join(ROOT_DIR, "samples\\load\\")
JSON = os.path.join(JSON1, "dataset\\")
JSON = "C:\\Users\jinwo\magicwand\source\\tan"
print(JSON)

annotations1 = json.load(open(os.path.join(JSON, "via_region_data.json")))
annotations2 = json.load(open(os.path.join(JSON, "via_region_data (2).json")))


'''
assert sel in ["train", "val"]
if sel == "train":
    JSON = os.path.join(JSON, "train\\")
    annotations1 = json.load(open(os.path.join(JSON, "via_region_data.json")))
else:
    JSON = os.path.join(JSON, "val\\")
    annotations1 = json.load(open(os.path.join(JSON, "via_region_data.json")))

assert sel in ["train", "val"]
if sel == "train":
    annotations2 = json.load(open(os.path.join(JSON, "via_region_data (2).json")))
else:
    annotations2 = json.load(open(os.path.join(JSON, "via_region_data (2).json")))
'''
print(annotations1, "\n", annotations2)
#print(json.dumps(annotations1, indent="\t"))
annotations1.update(annotations2)
#print(json.dumps(annotations1, indent="\t"))

with open("new_via_region_data.json", "w") as new: # 새 json 파일 쓰기
    json.dump(annotations1, new) #, indent="\t"      <- json 파일에 indentation을 할때

print("updated : ", annotations1)
