import json
from typing import Iterable
from urllib.parse import urlencode

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

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(UniversitySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)

    def start_requests(self) -> Iterable[Request]:
        for university_id, university_name in UNIVERSITY_META.items():
            model = University()
            model['zh_name'] = university_name
            model['id'] = university_id
            model['logo'] = f'https://static-data.gaokao.cn/upload/logo/{university_id}.jpg'

            yield Request(url=f'https://static-data.gaokao.cn/www/2.0/school/{model["id"]}/info.json',
                          callback=self.parse_university_detail,
                          cb_kwargs={'university': model})
            yield Request(url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/news/list.json',
                          callback=self.parse_news_list,
                          cb_kwargs={'university_id': university_id, 'api': True})

            # 院校分数线数据采集
            universityscore_q = init_universityscore_req_fn(university_id)
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(universityscore_q)}',
                callback=self.parse_university_score,
                cb_kwargs={'university_id': university_id, 'q': universityscore_q, 'api': True}
            )

            # 专业信息数据采集
            yield Request(
                url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/pc_special.json',
                callback=self.parse_university_professional,
                cb_kwargs={'university_id': university_id, 'api': True}
            )

            # 招生计划只采集山东的
            admissions_plan_q = init_admissionsplan_req_fn()
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(admissions_plan_q)}',
                callback=self.parse_admissions_plan_list,
                cb_kwargs={'q': admissions_plan_q, 'university_id': university_id, 'api': True, 'province_id': 37}
            )

            # 专业分数线数据采集
            major_score_q = init_majorscore_req_fn(university_id)
            yield Request(
                url=f'https://api.zjzw.cn/web/api/?{urlencode(major_score_q)}',
                callback=self.parse_major_score,
                cb_kwargs={'q': major_score_q, 'university_id': university_id, 'api': True}
            )

            # 就业指标数据采集
            yield Request(
                url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/pc_jobdetail.json',
                callback=self.parse_metric,
                cb_kwargs={'university_id': university_id}
            )
            break

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
        university = kwargs['university']

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_UNIVERSITY_DETAIL,
                                  university_id=university['id'],
                                  response=response)
            return

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

    def parse_university_professional(self, response: TextResponse, **kwargs):
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
                major = Major()
                major['course_category'] = course_category
                major['course_scopes'] = submajor['level2_name']
                major['id'] = submajor['id']
                major['university_id'] = university_id
                major['zh_name'] = submajor['special_name']
                major['edu_duration'] = submajor['limit_year']
                major['code'] = submajor['code']
                major['edu_level'] = submajor['type_name']
                yield Request(
                    url=f'https://static-data.gaokao.cn/www/2.0/school/{university_id}/special/{major["id"]}.json',
                    callback=self.parse_major_detail,
                    cb_kwargs={'major': major, 'university_id': university_id, 'api': True})

    def parse_major_detail(self, response: TextResponse, **kwargs):
        major = kwargs['major']
        university_id = kwargs['university_id']

        success, data = _parse_api_resp(resp_text=response.text)
        if not success:
            yield _make_apitarget(ApiTargetConsts.DESCRIBE_MAJOR_DETAIL,
                                  university_id=university_id,
                                  response=response)
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
                                  kwargs={
                                      'q': kwargs['q']
                                  })
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
                                  kwargs={
                                      'q': kwargs['q']
                                  })
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
                                  response=response)
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
