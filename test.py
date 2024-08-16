import json
import os
import sys

from jsonpath_ng import jsonpath, parse


def read_data():
    fp: str = f'{os.path.abspath(os.path.dirname(__file__))}/meta/school_major.json'
    with open(fp, 'r') as f:
        json_data = json.load(f)
        node_list: list = parse('$.school').find(json_data)
        s: jsonpath.DatumInContext = node_list[0]
        for school in s.value:
            print(school['school_id'])
            print(school['name'])

from universityspiders.settings import DOWNLOAD_DELAY



read_data()
