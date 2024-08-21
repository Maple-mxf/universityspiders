import os
import json
from jsonpath_ng import jsonpath, parse
from enum import Enum
import scrapy

from universityspiders.items import ErrorResponse


def read_university_meta():
    fp: str = f'{os.getcwd()}/meta/university_major.json'
    with open(fp, 'r') as f:
        json_data = json.load(f)
        university_node_list: list = parse('$.school').find(json_data)
        s: jsonpath.DatumInContext = university_node_list[0]

        ret = {}
        for university in s.value:
            ret[university['school_id']] = university['name']
        return ret


def read_province_mapping_meta() -> tuple:
    fp: str = f'{os.getcwd()}/meta/province.json'
    with open(fp, 'r') as f:
        json_data = json.load(f)
        arr = parse('$').find(json_data)[0].value

        p_province_mapping = {}
        r_province_mapping = {}
        for item in arr:
            p_province_mapping[item['provinceId']] = item['province']
            r_province_mapping[item['province']] = item['provinceId']

        return p_province_mapping, r_province_mapping


def read_university_detail_meta() -> dict:
    fp: str = f'{os.getcwd()}/meta/university_province.json'
    with open(fp, 'r') as f:
        json_data = json.load(f)
        kvs: dict = parse('$').find(json_data)[0].value
        return kvs


P_PROVINCE_MAPPING_META, R_PROVINCE_MAPPING_META = read_province_mapping_meta()
UNIVERSITY_META = read_university_meta()
UNIVERSITY_DETAIL_META = read_university_detail_meta()


# API AIN定义
class ApiTargetConsts(Enum):
    DESCRIBE_UNIVERSITY_DETAIL = 'DescribeUniversityDetail'
    DESCRIBE_NEWS_LIST = 'DescribeNewsList'
    DESCRIBE_NEWS_DETAIL = 'DescribeNewsDetail'
    DESCRIBE_UNIVERSITY_SCORE = 'DescribeUniversityScore'
    DESCRIBE_MAJOR_LIST = 'DescribeMajorList'
    DESCRIBE_MAJOR_DETAIL = 'DescribeMajorDetail'
    DESCRIBE_ADMISSIONS_PLAN_LIST = 'DescribeAdmissionsPlanList'
    DESCRIBE_MAJOR_SCORE_LIST = 'DescribeMajorScoreList'
    DESCRIBE_METRIC = 'DescribeMetric'


def _make_apitarget(api: ApiTargetConsts,
                    university_id: str,
                    response: scrapy.http.Response,
                    **kwargs):
    er = ErrorResponse()
    request: scrapy.Request = response.request
    er['api_name'] = api.value
    er['university_id'] = university_id
    er['url'] = request.url
    er['body'] = request.body
    er['method'] = request.method
    if kwargs:
        er['q'] = kwargs.get('q')
        er['kwargs'] = kwargs.get('kwargs', None)

    return er
