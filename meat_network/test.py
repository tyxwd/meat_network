# 处理并生成json数据
import json
import pandas
import re

dict_a = json.load(open("class_index_dict.json"))
for key, value in dict_a.items():
    print(key)
