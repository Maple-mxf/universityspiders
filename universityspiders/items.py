# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class University(scrapy.Item):
    id = scrapy.Field()
    zh_name = scrapy.Field()
    logo = scrapy.Field()

    official_website = scrapy.Field()
    admissions_contact_phone = scrapy.Field()
    admissions_contact_email = scrapy.Field()

    arwu_ranking = scrapy.Field()  # 软科排名
    aa_ranking = scrapy.Field()  # 校友会排名
    qs_ranking = scrapy.Field()  # QS排名
    usn_ranking = scrapy.Field()  # U.S. News世界大学排名
    the_ranking = scrapy.Field()  # 泰晤士大学排名
    # hot_ranking = scrapy.Field()  # 人气排名

    edu_level = scrapy.Field()  # 教育层次，A代表本科 B代表专科
    edu_category = scrapy.Field()  # 教育类别 A代表综合类 B代表理工类
    edu_establish = scrapy.Field()  # 办学性质 A代表公办
    tags = scrapy.Field()

    establish_time = scrapy.Field()  # 建校时间
    area = scrapy.Field()  # 面积
    mgr_dept = scrapy.Field()  # 主管部门
    address = scrapy.Field()

    doctoral_program_num = scrapy.Field()  # 博士点总数
    master_program_num = scrapy.Field()  # 硕士点总数
    important_subject_num = scrapy.Field()  # 重点学科数量

    province_id = scrapy.Field()
    province_name = scrapy.Field()
    city_name = scrapy.Field()
    city_id = scrapy.Field()
    county_name = scrapy.Field()
    county_id = scrapy.Field()
    town_name = scrapy.Field()

    introduction = scrapy.Field()

    f985 = scrapy.Field()
    f211 = scrapy.Field()


class Major(scrapy.Item):
    id = scrapy.Field()
    zh_name = scrapy.Field()
    code = scrapy.Field()
    edu_level = scrapy.Field()
    course_scopes = scrapy.Field()
    course_category = scrapy.Field()
    edu_duration = scrapy.Field()  # 学制
    graduate = scrapy.Field()  # 授予学位
    introduction = scrapy.Field()
    university_id = scrapy.Field()


class MajorScore(scrapy.Item):
    str_id = scrapy.Field()
    subject_name = scrapy.Field()  # 学科
    avg = scrapy.Field()  # 平均分
    max = scrapy.Field()  # 最高分
    min = scrapy.Field()  # 最低分
    min_ranking = scrapy.Field()  # 最低位次

    batch_num_name = scrapy.Field()  # 本科1批 本科2批

    subject_scopes_name = scrapy.Field()
    subject_category_name = scrapy.Field()

    major_id = scrapy.Field()
    university_id = scrapy.Field()
    year = scrapy.Field()

    province_id = scrapy.Field()
    province_name = scrapy.Field()

    min_range = scrapy.Field()
    min_rank_range = scrapy.Field()


class AdmissionsPlan(scrapy.Item):
    major_name = scrapy.Field()
    admissions_stu_num = scrapy.Field()

    edu_fee = scrapy.Field()

    university_id = scrapy.Field()

    major_code = scrapy.Field()

    batch_num_name = scrapy.Field()  # 本科1批 本科2批
    subject_name = scrapy.Field()  # 学科 文科理科

    year = scrapy.Field()

    province_id = scrapy.Field()
    province_name = scrapy.Field()

    cond = scrapy.Field()  # 选科要求
    edu_dur = scrapy.Field()  # 学制 4年 ｜ 5年


class AdmissionsNews(scrapy.Item):
    id = scrapy.Field()
    university_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    type_id = scrapy.Field()
    type_name = scrapy.Field()
    publish_date = scrapy.Field()


class UniversityScore(scrapy.Item):
    year = scrapy.Field()
    admissions_batch_num = scrapy.Field()  # 录取批次
    admissions_type = scrapy.Field()  # 招生类型 普通类 ｜ 地方专项计划	｜ 国家专项计划
    min = scrapy.Field()  # 最低分  TODO 这里的最低分可能是个 -
    min_ranking = scrapy.Field()  # 最低位次

    max = scrapy.Field()
    avg = scrapy.Field()
    avg_ranking = scrapy.Field()

    province_id = scrapy.Field()
    province_name = scrapy.Field()

    subject_category = scrapy.Field()
    province_control_score = scrapy.Field()
    university_id = scrapy.Field()

    cond = scrapy.Field()
    major_group_id = scrapy.Field()
    major_group_name = scrapy.Field()


class EmploymentRegionRateMetric(scrapy.Item):
    university_id = scrapy.Field()
    rate = scrapy.Field()
    province_name = scrapy.Field()
    year = scrapy.Field()


class CompanyAttrRateMetric(scrapy.Item):
    name = scrapy.Field()
    rate = scrapy.Field()
    university_id = scrapy.Field()


class CompanyMetric(scrapy.Item):
    university_id = scrapy.Field()
    name = scrapy.Field()
    sort = scrapy.Field()


class ErrorResponse(scrapy.Item):
    api_name = scrapy.Field()
    university_id = scrapy.Field()
    url = scrapy.Field()
    q = scrapy.Field()
    method = scrapy.Field()
    ctx_id = scrapy.Field()
    body = scrapy.Field()
