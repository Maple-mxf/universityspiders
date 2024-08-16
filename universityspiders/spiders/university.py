import json
import os

from typing import Iterable, Any
from urllib.parse import urlencode

import scrapy
from scrapy import signals, Request, Selector
from scrapy.http import HtmlResponse, TextResponse
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as matcher
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from jsonpath_ng import jsonpath, parse

from universityspiders.items import University, Major, MajorScore, UniversityAdmissionsPlan


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


class UniversitySpider(scrapy.Spider):
    name = "university"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--proxy-server=http://127.0.0.1:7890")
        self.driver = Chrome(chrome_options)

        # self.driver.get('https://www.gaokao.cn/school/search')
        #
        # qrcode = WebDriverWait(self.driver, 60, 3).until(
        #     matcher.presence_of_element_located((By.CLASS_NAME, 'login-popup_loginPopup__d_xjJ')))
        # print('请扫描二维码...')
        #
        # WebDriverWait(self.driver, 300, 3).until(
        #     matcher.invisibility_of_element_located((By.CLASS_NAME, 'login-popup_loginPopup__d_xjJ'))
        # )
        # print('登录成功！')
        self.university_meta = read_university_meta()
        self.p_province_mapping, self.r_province_mapping = read_province_mapping_meta()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(UniversitySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)
        # spider.driver.quit()

    def start_requests(self) -> Iterable[Request]:
        for university_id, university_name in self.university_meta.items():
            model = University()
            model['zh_name'] = university_name
            model['id'] = university_id

            yield Request(url=f'https://www.gaokao.cn/school/{model["id"]}',
                          callback=self.parse_university_detail,
                          cb_kwargs={
                              'university': model
                          })
            break  # TODO

    def parse_university_detail(self, response: HtmlResponse, **kwargs):
        university = kwargs['university']
        sel = Selector(response)
        baseinfo_node_list = sel.xpath(
            '//div[starts-with(@class,"school-tab_labelBox")]/div[starts-with(@class,"school-tab_item")]')
        university['official_website'] = baseinfo_node_list[0].css('div::text').extract_first()
        university['admission_contact_phone'] = baseinfo_node_list[1].css('div::text').extract_first()
        university['admission_contact_email'] = baseinfo_node_list[2].css('div::text').extract_first()

        ranking_node_list = sel.xpath('//div[starts-with(@class,"shcool-rank_item")]')
        university['arwu_ranking'] = ranking_node_list[0].css('span::text').extract_first()
        university['aa_ranking'] = ranking_node_list[1].css('span::text').extract_first()
        university['usn_ranking'] = ranking_node_list[2].css('span::text').extract_first()
        university['hot_ranking'] = ranking_node_list[3].css('span::text').extract_first()

        tag_node_list = sel.xpath(
            '//div[starts-with(@class,"school-tab_tags")]/div[starts-with(@class,"school-tab_item")]')
        university['edu_level'] = tag_node_list[0].css('div::text').extract_first()
        university['edu_category'] = tag_node_list[1].css('div::text').extract_first()
        university['edu_establish'] = tag_node_list[2].css('div::text').extract_first()
        university['tags'] = [item.css('div::text').extract() for item in tag_node_list]

        des_node_list = sel.xpath('//div[@class="school-tags-des"]/div')
        university['establish_time'] = des_node_list[0].css('span::text').extract_first()
        university['area'] = des_node_list[1].css('span::text').extract_first()
        university['mgr_dept'] = des_node_list[2].css('span::text').extract_first()
        university['address'] = des_node_list[3].css('span::text').extract_first()

        baseinfo2_node_list = sel.xpath('//div[@class="base_info_item_top clearfix"]')
        if len(baseinfo2_node_list) >= 2:
            university['doctoral_program_num'] = baseinfo2_node_list[1].css('div::text').extract_first()
        if len(baseinfo2_node_list) >= 3:
            university['master_program_num'] = baseinfo2_node_list[2].css('div::text').extract_first()
        if len(baseinfo2_node_list) >= 3:
            university['important_score_num'] = baseinfo2_node_list[3].css('div::text').extract_first()

        yield Request(
            url=f'https://static-data.gaokao.cn/www/2.0/school/{university["id"]}/detail/69000.json',
            callback=self.parse_university_intro,
            cb_kwargs={'university': university, 'api': True}
        )

        yield Request(
            url=f'https://static-data.gaokao.cn/www/2.0/school/{university["id"]}/pc_special.json',
            callback=self.parse_university_professional,
            cb_kwargs={'university_id': university['id'], 'api': True}
        )

        for req in self.create_major_score_reqs(university['id']):
            yield req

        for province_id in self.p_province_mapping:
            for req in self.create_admissions_plan_reqs(university['id'], province_id):
                yield req

    def create_major_score_reqs(self, university_id) -> Iterable[Request]:
        major_score_q = {
            # 'local_province_id': province_id,
            'page': 1,
            'size': 20,
            'school_id': university_id,
            'special_group': '',
            'uri': 'apidata/api/gk/score/special'
        }
        req_qs = []
        lk_major_score_q = {'local_type_id': 1}
        for k, v in major_score_q.items():
            lk_major_score_q[k] = v

        wk_major_score_q = {'local_type_id': 2}
        for k, v in major_score_q.items():
            wk_major_score_q[k] = v

        req_qs.append(lk_major_score_q)
        req_qs.append(wk_major_score_q)

        for q in req_qs:
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(q)}',
                callback=self.parse_major_score,
                cb_kwargs={'q': major_score_q, 'university_id': university_id, 'api': True}
            )

    def create_admissions_plan_reqs(self, university_id, province_id) -> Iterable[Request]:
        admissions_plan_q = {
            'local_province_id': province_id,
            'school_id': university_id,
            'size': 20,
            'page': 1,
            'special_group': '',
            'uri': 'apidata/api/gkv3/plan/school'
        }

        req_qs = []
        lk_admissions_plan_q = {'local_type_id': 1}
        for k, v in admissions_plan_q.items():
            lk_admissions_plan_q[k] = v
        wk_admissions_plan_q = {'local_type_id': 2}
        for k, v in admissions_plan_q.items():
            wk_admissions_plan_q[k] = v

        req_qs.append(lk_admissions_plan_q)
        req_qs.append(wk_admissions_plan_q)

        for q in req_qs:
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(q)}',
                callback=self.parse_admissions_plan_list,
                cb_kwargs={'q': q, 'university_id': university_id, 'api': True, 'province_id': province_id}
            )

    def parse_university_intro(self, response: TextResponse, **kwargs):
        university = kwargs['university']
        json_data = json.loads(response.body)
        university['introduction'] = parse('$.data.content').find(json_data)[0].value
        yield university

    def parse_university_professional(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        json_data = json.loads(response.body)

        node_list: list = parse('$.data.special').find(json_data)
        for category in node_list[0].value:
            course_category = category['name']
            for submajor in category['special']:
                major = Major()
                major['course_category'] = course_category
                major['course_scopes'] = submajor['level2_name']
                major['id'] = submajor['id']
                major['university_id'] = university_id
                major['zh_name'] = submajor['special_name']
                major['edu_duration'] = submajor['limit_year']
                major['code'] = submajor['code']
                yield Request(
                    url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/special/{major["id"]}.json',
                    callback=self.parse_major_detail,
                    cb_kwargs={
                        'major': major,
                        'university_id': university_id,
                        'api': True
                    }
                )

                break
            break

    def parse_major_detail(self, response: TextResponse, **kwargs):
        major = kwargs['major']
        json_data = json.loads(response.body)
        major['introduction'] = parse('$.data.content').find(json_data)[0].value
        yield major

    def parse_major_score(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        json_data = json.loads(response.body)

        resp_code = parse('$.code').find(json_data)[0].value
        if resp_code == '1069':
            print(f'parse_major_score#Request URL = {response.url}, cb_kwargs = {response.cb_kwargs}')
            return

        major_score_list: list = parse('$.data.item').find(json_data)[0].value

        for item in major_score_list:
            major_score = MajorScore()
            major_score['university_id'] = university_id
            major_score['major_id'] = item['special_id']
            major_score['year'] = item['year']
            major_score['str_id'] = item['id']
            major_score['subject_name'] = item['local_type_name']
            major_score['average'] = item['average']
            major_score['max'] = item['max']
            major_score['min'] = item['min']
            major_score['batch_num_name'] = item['local_batch_name']

            major_score['course_scopes_name'] = item['level2_name']
            major_score['course_category_name'] = item['level3_name']

            major_score['province_name'] = item.get('local_province_name', '')
            major_score['province_id'] = self.r_province_mapping.get(major_score['province_name']) or ''

            yield major_score

        q: dict = kwargs['q']
        page: int = q['page']
        count: int = parse('$.data.numFound').find(json_data)[0].value
        if len(major_score_list) >= 20 and count > page * 20:
            q['page'] = page + 1
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(q)}',
                callback=self.parse_major_score,
                cb_kwargs={'q': q, 'university_id': university_id, 'api': True}
            )

    def parse_admissions_plan_list(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        province_id = kwargs['province_id']
        json_data = json.loads(response.body)
        resp_code = parse('$.code').find(json_data)[0].value
        if resp_code == '1069':
            print(f'parse_major_score#Request URL = {response.url}, cb_kwargs = {response.cb_kwargs}')
            return
        plan_list = parse('$.data.item').find(json_data)[0].value
        for plan in plan_list:
            admissions_plan = UniversityAdmissionsPlan()
            admissions_plan['major_name'] = plan['spname']
            admissions_plan['admissions_stu_num'] = plan['num']

            admissions_plan['university_id'] = plan['school_id']
            admissions_plan['major_code'] = plan['spcode']
            admissions_plan['batch_num_name'] = plan['local_batch_name']
            admissions_plan['subject_name'] = plan['local_type_name']
            admissions_plan['year'] = plan['year']
            admissions_plan['edu_fee'] = plan['tuition']

            admissions_plan['province_id'] = province_id
            admissions_plan['province_name'] = self.p_province_mapping[province_id]

            yield admissions_plan

        q: dict = kwargs['q']
        page: int = q['page']
        count: int = parse('$.data.numFound').find(json_data)[0].value
        if len(plan_list) >= 20 and count > page * 20:
            q['page'] = page + 1
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(q)}',
                callback=self.parse_admissions_plan_list,
                cb_kwargs={
                    'q': q,
                    'university_id': university_id,
                    'api': True,
                    'province_id': province_id
                }
            )
