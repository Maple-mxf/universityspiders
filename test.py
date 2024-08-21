import json
from jsonpath_ng import parse

# (1062, "Duplicate entry '140-2021-本科批-普通类-32-物理类' for key 'university_score.idx'")
# 140-2022-本科批-普通类-11-综合-51416
with open('data.json', mode='r', encoding='utf=8') as file:
    datalist = json.load(file)

    print(len(datalist))

    js_datalist = [item for item in datalist if item['local_province_name'] == '北京' and item['year'] == 2022 and item[
        'sg_info'] == '物理、化学(2科必选)']

    with open('js_data.json', mode='w', encoding='utf-8') as f2:
        json.dump(js_datalist, f2, indent=4, ensure_ascii=False)
