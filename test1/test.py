# 处理并生成json数据
import json


all_classes = []
with open("configuration.txt") as fb:
    all_classes = fb.readlines()
for i in range(len(all_classes)):
    all_classes[i] = all_classes[i].strip()
# print(all_classes)

c_n = []
with open("C_N.txt") as fobj:
    c_n = fobj.readlines()

for i in range(len(c_n)):
    c_n[i] = c_n[i].strip()

class_CN_dict = dict(zip(all_classes, c_n))
class_CN_json = json.dumps(class_CN_dict)

with open("class_CN_dict.json", "w", encoding="utf-8") as js_:

    js_.writelines(class_CN_json)
# all_index = []
# for i in range(23):
#     txt = "CLASS" + str(i + 1)
#     all_index.append(txt)
#
# class_index_dict = dict(zip(all_classes, all_index))
# class_index_json = json.dumps(class_index_dict)
#
# with open("class_index_dict.json", "w", encoding="utf-8") as js_:
#
#     js_.writelines(class_index_json)

a = json.load(open("class_index_dict.json"))
print(a)