import json
from typing import Iterable
from urllib.parse import urlencode

import pymysql
import scrapy
from jsonpath_ng import parse
from scrapy import (
    signals,
    Request
)
from scrapy.http import (
    HtmlResponse,
    TextResponse
)
from scrapy.utils.project import get_project_settings

from universityspiders import (
    UNIVERSITY_META,
    P_PROVINCE_MAPPING_META,
    R_PROVINCE_MAPPING_META,
    _make_apitarget,
    ApiTargetConsts
)
from universityspiders.items import (
    University,
    Major,
    MajorScore,
    AdmissionsPlan,
    AdmissionsNews,
    UniversityScore,
    EmploymentRegionRateMetric,
    CompanyAttrRateMetric,
    CompanyMetric
)
from universityspiders.spiders import (
    _parse_api_resp,
    init_majorscore_req_fn,
    init_admissionsplan_req_fn,
    init_universityscore_req_fn
)


class UniversitySpider(scrapy.Spider):
    name = "university"

    def __init__(self, restore=None, ctx_id: str = None, **kwargs):
        super().__init__(**kwargs)
        self.restore = restore
        self.ctx_id = ctx_id

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(UniversitySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)

    def start_requests(self) -> Iterable[Request]:
        if self.restore is 'T' and self.ctx_id and len(self.ctx_id) > 0:
            for request in self.restore_requests():
                yield request
        else:
            for university_id, university_name in UNIVERSITY_META.items():
                # 学校详细信息数据采集
                yield self.make_university_detail_request(university_id,
                                                          f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/info.json')

                # 招生咨询数据采集
                yield self.make_news_list_request(university_id,
                                                  f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/news/list.json')

                # 院校分数线数据采集
                universityscore_q = init_universityscore_req_fn(university_id)
                yield self.make_university_score_request(university_id,
                                                         f'https://api.zjzw.cn/web/api/?{urlencode(universityscore_q)}',
                                                         universityscore_q)
                # 专业信息数据采集
                yield self.make_major_list_request(university_id,
                                                   f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/pc_special.json')

                # 招生计划只采集山东的
                admissions_plan_q = init_admissionsplan_req_fn(university_id, 37)
                yield self.make_admissions_plan_list_request(
                    university_id,
                    f'https://api.zjzw.cn/web/api/?{urlencode(admissions_plan_q)}',
                    **{'province_id': 37, 'q': admissions_plan_q}
                )

                # 专业分数线数据采集
                major_score_q = init_majorscore_req_fn(university_id)
                yield self.make_major_score_list_request(
                    university_id,
                    f'https://api.zjzw.cn/web/api/?{urlencode(major_score_q)}',
                    **{'q': major_score_q}
                )

                # 就业指标数据采集
                self.make_employment_metric_request(university_id,
                                                    f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/pc_jobdetail.json')
                break

    def make_university_detail_request(self, university_id, url):
        return Request(url=url,
                       callback=self.parse_university_detail,
                       cb_kwargs={'university_id': university_id})

    def make_news_list_request(self, university_id, url):
        return Request(url=url,
                       callback=self.parse_news_list,
                       cb_kwargs={'university_id': university_id, 'api': True})

    def make_news_detail_request(self, university_id, url):
        return Request(
            url=url,
            callback=self.parse_news_detail,
            cb_kwargs={'university_id': university_id, 'api': True}
        )

    def make_university_score_request(self, university_id, url, q) -> scrapy.Request:
        return Request(
            url=url,
            callback=self.parse_university_score,
            cb_kwargs={'university_id': university_id, 'q': q, 'api': True}
        )

    def make_major_list_request(self, university_id, url) -> scrapy.Request:
        return Request(
            url=url,
            callback=self.parse_university_major,
            cb_kwargs={'university_id': university_id, 'api': True}
        )

    def make_major_detail_request(self, university_id, url, submajor, course_category) -> scrapy.Request:
        return Request(
            url=url,
            callback=self.parse_major_detail,
            cb_kwargs={'submajor': submajor,
                       'course_category': course_category,
                       'university_id': university_id,
                       'api': True})

    def make_admissions_plan_list_request(self, university_id, url, q, province_id) -> scrapy.Request:
        return Request(
            url=url,
            callback=self.parse_admissions_plan_list,
            cb_kwargs={'q': q, 'university_id': university_id, 'api': True, 'province_id': province_id}
        )

    def make_major_score_list_request(self, university_id, url, q) -> scrapy.Request:
        return Request(
            url=url,
            callback=self.parse_major_score,
            cb_kwargs={'q': q, 'university_id': university_id, 'api': True}
        )

    def make_employment_metric_request(self, university_id, url) -> scrapy.Request:
        return Request(
            url=url,
            callback=self.parse_metric,
            cb_kwargs={'university_id': university_id}
        )

    def restore_requests(self) -> Iterable[Request]:
        settings = get_project_settings()
        host = settings.get(name='DB_HOST', default='127.0.0.1')
        port = settings.get(name='DB_PORT', default=3306)
        user = settings.get(name='DB_USER', default='root')
        pwd = settings.get(name='DB_PWD', default='123456')
        db = settings.get(name='DB_DATABASE', default='universityspiders')
        conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               password=pwd,
                               database=db)
        cursor = conn.cursor()

        cursor.execute('select api_name, university_id, url, ctx_para from error_response where ctx_id=%s',
                       (self.ctx_id))
        error_resp_list = cursor.fetchall()

        for error_resp in error_resp_list:
            apiname = error_resp[0]
            university_id = error_resp[1]
            url = error_resp[2]
            kwargs_str = error_resp[3]
            if apiname == ApiTargetConsts.DESCRIBE_UNIVERSITY_DETAIL.value:
                yield self.make_university_detail_request(university_id, url)
            elif apiname == ApiTargetConsts.DESCRIBE_NEWS_LIST.value:
                yield self.make_news_list_request(university_id, url)
            elif apiname == ApiTargetConsts.DESCRIBE_NEWS_DETAIL.value:
                yield self.make_news_detail_request(university_id, url)
            elif apiname == ApiTargetConsts.DESCRIBE_UNIVERSITY_SCORE.value:
                kwargs = json.loads(kwargs_str)
                yield self.make_university_score_request(university_id, url, **kwargs)
            elif apiname == ApiTargetConsts.DESCRIBE_MAJOR_LIST.value:
                yield self.make_major_list_request(university_id, url)
            elif apiname == ApiTargetConsts.DESCRIBE_MAJOR_DETAIL.value:
                kwargs = json.loads(kwargs_str)
                yield self.make_major_detail_request(
                    university_id, url, **kwargs)
            elif apiname == ApiTargetConsts.DESCRIBE_ADMISSIONS_PLAN_LIST.value:
                kwargs = json.loads(kwargs_str)
                yield self.make_admissions_plan_list_request(university_id, url, **kwargs)
            elif apiname == ApiTargetConsts.DESCRIBE_MAJOR_SCORE_LIST.value:
                kwargs = json.loads(kwargs_str)
                yield self.make_major_score_list_request(university_id, url, **kwargs)
            elif apiname == ApiTargetConsts.DESCRIBE_METRIC.value:
                yield self.make_employment_metric_request(university_id, url)

        conn.close()
        """"""

    def parse_news_list(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']

        success, newslist = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_NEWS_DETAIL,
                                  university_id=university_id,
                                  response=response)
            return

        for news in newslist:
            yield Request(
                url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/news/{news["type"]}/{news["id"]}.json',
                callback=self.parse_news_detail,
                cb_kwargs={'university_id': university_id, 'api': True}
            )

    def parse_news_detail(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        news = AdmissionsNews()

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_NEWS_DETAIL,
                                  university_id,
                                  response)
            return

        news['id'] = data.get('id')
        news['university_id'] = university_id
        news['title'] = data.get('title', '')
        news['content'] = data.get('content', '')
        news['type_id'] = data.get('type', '')
        news['type_name'] = data.get('type_name', '')
        news['publish_date'] = data.get('add_time', None)

        yield news

    def parse_university_detail(self, response: HtmlResponse, **kwargs):
        university_id = kwargs['university_id']

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_UNIVERSITY_DETAIL,
                                  university_id=university_id,
                                  response=response)
            return

        university = University()
        university['zh_name'] = data.get('name')
        university['id'] = university_id
        university['logo'] = f'https://static-data.gaokao.cn/upload/logo/{university_id}.jpg'

        university['official_website'] = ','.join(
            [data.get('site', ''), data.get('school_site', '')]
        )
        university['admissions_contact_phone'] = data.get('phone', '')
        university['admissions_contact_email'] = data.get('email', '')

        university['edu_level'] = data.get('level_name', '')
        university['edu_category'] = data.get('type_name', '')
        university['edu_establish'] = data.get('nature_name', '')
        university['f211'] = data.get('f211', '0')
        university['f985'] = data.get('f985', '0')

        university['mgr_dept'] = data.get('belong', '')
        university['establish_time'] = data.get('create_date', '')
        university['area'] = data.get('area', '')
        university['address'] = data.get('address', '')

        university['province_name'] = data.get('province_name', '')
        university['province_id'] = data.get('province_id', '')
        university['city_name'] = data.get('city_name', '')
        university['city_id'] = data.get('city_id', '')
        university['city_id'] = data.get('city_id', '')
        university['county_id'] = data.get('county_id', '')
        university['town_name'] = data.get('town_name', '')

        # TODO school_batch字段是用于查询接口？
        university['doctoral_program_num'] = data.get('num_doctor', '0')
        university['master_program_num'] = data.get('num_master', '0')
        university['important_subject_num'] = data.get('num_subject', '0')

        rank = data['rank']
        if rank:
            university['arwu_ranking'] = rank.get('ruanke_rank', '')
            university['aa_ranking'] = rank.get('xyh_rank', '')
            university['qs_ranking'] = rank.get('qs_world', '')
            university['usn_ranking'] = rank.get('us_rank', '')
            university['the_ranking'] = rank.get('tws_china', '')

        yield Request(
            url=f'https://static-data.gaokao.cn/www/2.0/school/{university["id"]}/detail/69000.json',
            callback=self.parse_university_intro,
            cb_kwargs={'university': university, 'api': True}
        )

    def parse_university_intro(self, response: TextResponse, **kwargs):
        university = kwargs['university']
        json_data = json.loads(response.body)
        university['introduction'] = parse('$.data.content').find(json_data)[0].value
        yield university

    def parse_university_major(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_MAJOR_LIST,
                                  university_id=university_id,
                                  response=response)
            return

        node_list: list = data.get('special', [])
        for category in node_list[0].value:
            course_category = category['name']
            for submajor in category['special']:
                yield Request(
                    url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/special/{submajor["id"]}.json',
                    callback=self.parse_major_detail,
                    cb_kwargs={'course_category': course_category,
                               'submajor': submajor,
                               'university_id': university_id,
                               'api': True})

    def parse_major_detail(self, response: TextResponse, **kwargs):
        submajor = kwargs['submajor']
        course_category = kwargs['course_category']
        university_id = kwargs['university_id']

        major = Major()
        major['course_category'] = course_category
        major['course_scopes'] = submajor['level2_name']
        major['id'] = submajor['id']
        major['university_id'] = university_id
        major['zh_name'] = submajor['special_name']
        major['edu_duration'] = submajor['limit_year']
        major['code'] = submajor['code']
        major['edu_level'] = submajor['type_name']

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_MAJOR_DETAIL,
                                  university_id=university_id,
                                  response=response,
                                  submajor=submajor,
                                  course_category=course_category)
            return

        json_data = json.loads(response.body)
        data = parse('$.data').find(json_data)[0].value
        major['introduction'] = data.get('content', '')
        major['graduate'] = data.get('degree', '')
        yield major

    def parse_major_score(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_MAJOR_SCORE_LIST,
                                  university_id=university_id,
                                  response=response,
                                  q=kwargs['q'])
            return

        major_score_list: list = data.get('item', [])

        for item in major_score_list:
            major_score = MajorScore()
            major_score['university_id'] = university_id
            major_score['major_id'] = item['special_id']
            major_score['year'] = item['year']
            major_score['str_id'] = item['id']
            major_score['subject_name'] = item['local_type_name']
            major_score['avg'] = item['average']
            major_score['max'] = item['max']
            major_score['min'] = item['min']
            major_score['min_ranking'] = item['min_section']
            major_score['batch_num_name'] = item['local_batch_name']

            major_score['subject_scopes_name'] = item['level2_name']
            major_score['subject_category_name'] = item['level3_name']

            major_score['province_name'] = item.get('local_province_name', '')
            major_score['province_id'] = R_PROVINCE_MAPPING_META.get(major_score['province_name']) or ''

            major_score['min_range'] = item.get('min_range', '')
            major_score['min_rank_range'] = item.get('min_rank_range', '')

            yield major_score

        q: dict = kwargs['q']
        page: int = q['page']
        if len(major_score_list) >= 20:
            q['page'] = page + 1
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(q)}',
                callback=self.parse_major_score,
                cb_kwargs={'q': q, 'university_id': university_id, 'api': True}
            )

    def parse_admissions_plan_list(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        province_id = kwargs['province_id']

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_ADMISSIONS_PLAN_LIST,
                                  university_id=university_id,
                                  response=response,
                                  q=kwargs['q'],
                                  province_id=province_id)
            return

        plan_list = data.get('item', [])
        for plan in plan_list:
            admissions_plan = AdmissionsPlan()
            admissions_plan['major_name'] = plan['spname']
            admissions_plan['admissions_stu_num'] = plan['num']

            admissions_plan['university_id'] = plan['school_id']
            admissions_plan['major_code'] = plan['spcode']
            admissions_plan['batch_num_name'] = plan['local_batch_name']
            admissions_plan['subject_name'] = plan['local_type_name']
            admissions_plan['year'] = plan['year']
            admissions_plan['edu_fee'] = plan['tuition']

            admissions_plan['province_id'] = province_id
            admissions_plan['province_name'] = P_PROVINCE_MAPPING_META[province_id]

            admissions_plan['cond'] = plan['sp_info']
            admissions_plan['edu_dur'] = plan['length']

            yield admissions_plan

        q: dict = kwargs['q']
        page: int = q['page']
        if len(plan_list) >= 20:
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

    def parse_university_score(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        success, payload = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_UNIVERSITY_SCORE,
                                  university_id=university_id,
                                  response=response,
                                  q=kwargs['q'])
            return

        itemlist = payload['item']

        for item in itemlist:
            us = UniversityScore()
            us['university_id'] = university_id
            us['year'] = item.get('year')
            us['admissions_batch_num'] = item.get('local_batch_name')
            us['admissions_type'] = item.get('zslx_name')
            us['min'] = item.get('min')
            us['min_ranking'] = item.get('min_section')
            us['max'] = item.get('max')
            us['province_name'] = item.get('local_province_name')
            us['province_control_score'] = item.get('proscore')
            us['subject_category'] = item.get('local_type_name')
            us['province_id'] = R_PROVINCE_MAPPING_META.get(item.get('local_province_name'))
            us['cond'] = item.get('sg_info')
            us['major_group_id'] = item.get('special_group')
            us['major_group_name'] = item.get('sg_name')

            yield us

        if len(itemlist) >= 20:
            q = kwargs['q']
            q['page'] = q['page'] + 1
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(q)}',
                callback=self.parse_university_score,
                cb_kwargs={'university_id': university_id, 'q': q, 'api': True})

    def parse_metric(self, response: TextResponse, **kwargs):
        university_id = kwargs['university_id']
        success, payload = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(
                ApiTargetConsts.DESCRIBE_METRIC,
                university_id=university_id,
                response=response
            )
            return

        if payload is None:
            return

        region_metric = payload.get('province')
        if region_metric is not None:
            for item in region_metric:
                m = EmploymentRegionRateMetric()
                m['university_id'] = university_id
                m['province_name'] = item.get('province_name')
                m['year'] = item.get('year')
                m['rate'] = item.get('rate')
                yield m

        company_attr_metric = payload.get('attr')
        if company_attr_metric is not None:
            for k, v in company_attr_metric.items():
                m = CompanyAttrRateMetric()
                m['university_id'] = university_id
                m['name'] = k
                m['rate'] = v
                yield m

        company_metric = payload.get('company')
        if company_metric is not None:
            for k, v in company_metric.items():
                m = CompanyMetric()
                m['university_id'] = university_id
                m['name'] = k
                m['sort'] = v
                yield m
