# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class University(scrapy.Item):
    id = scrapy.Field()
    zh_name = scrapy.Field()
    logo = scrapy.Field()
    hot = scrapy.Field()

    official_website = scrapy.Field()
    admission_contact_phone = scrapy.Field()
    admission_contact_email = scrapy.Field()

    arwu_ranking = scrapy.Field()  # 软科排名
    aa_ranking = scrapy.Field()  # 校友会排名
    qs_ranking = scrapy.Field()  # QS排名
    usn_ranking = scrapy.Field()  # U.S. News世界大学排名
    hot_ranking = scrapy.Field()  # 人气排名
    edu_level = scrapy.Field()  # 教育层次，A代表本科 B代表专科
    edu_category = scrapy.Field()  # 教育层次，A代表本科 B代表专科
    edu_establish = scrapy.Field()  # 办学性质 A代表公办
    tags = scrapy.Field()

    establish_time = scrapy.Field()  # 建校时间
    area = scrapy.Field()  # 面积
    mgr_dept = scrapy.Field()  # 主管部门
    address = scrapy.Field()

    doctoral_program_num = scrapy.Field()  # 博士点总数
    master_program_num = scrapy.Field()  # 硕士点总数
    important_score_num = scrapy.Field()  # 重点学科数量

    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()

    introduction = scrapy.Field()


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
    average = scrapy.Field()  # 平均分
    max = scrapy.Field()  # 最高分
    min = scrapy.Field()  # 最低分

    batch_num_name = scrapy.Field()  # 本科1批 本科2批

    course_scopes_name = scrapy.Field()
    course_category_name = scrapy.Field()

    major_id = scrapy.Field()
    university_id = scrapy.Field()
    year = scrapy.Field()

    province_id = scrapy.Field()
    province_name = scrapy.Field()


class UniversityAdmissionsPlan(scrapy.Item):
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
