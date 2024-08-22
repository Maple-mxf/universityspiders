import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from universityspiders.items import (
    University,
    Major,
    MajorScore,
    AdmissionsPlan,
    AdmissionsNews,
    UniversityScore,
    EmploymentRegionRateMetric,
    CompanyAttrRateMetric,
    CompanyMetric,
    ErrorResponse
)
import pymysql
from scrapy.utils.project import get_project_settings


class Write2DBPipeline:
    def __init__(self):
        settings = get_project_settings()
        host = settings.get(name='DB_HOST', default='127.0.0.1')
        port = settings.get(name='DB_PORT', default=3306)
        user = settings.get(name='DB_USER', default='root')
        pwd = settings.get(name='DB_PWD', default='123456')
        db = settings.get(name='DB_DATABASE', default='universityspiders')

        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=pwd,
                                    database=db)
        self.cursor = self.conn.cursor()
        self.data = []

    def write_batch_data(self):
        pass

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.write_batch_data()
            self.conn.commit()
        self.conn.close()
        pass


class UniversityPipeline(Write2DBPipeline):
    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, University):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        self._execute_sqlscript(item)
        return item

    def _execute_sqlscript(self, item: scrapy.Item):
        sqlscript = """
        insert into university(id, zh_name, logo, official_website, admissions_contact_phone, admissions_contact_email,
                       arwu_ranking, aa_ranking, qs_ranking, usn_ranking, the_ranking, edu_level, edu_category,
                       edu_establish, tags, establish_time, area, mgr_dept, address, doctoral_program_num,
                       master_program_num, important_subject_num, province_id, province_name, city_name, city_id,
                       county_name, county_id, town_name, introduction, f985, f211)
        values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s,%s)
        on duplicate key update 
        zh_name= %s,  
        logo= %s,  
        official_website= %s, 
        admissions_contact_phone= %s,  
        admissions_contact_email= %s,  
        arwu_ranking= %s,  
        aa_ranking= %s,  
        qs_ranking= %s,  
        usn_ranking= %s,  
        the_ranking= %s,  
        edu_level= %s,  
        edu_category= %s,  
        edu_establish= %s,  
        tags= %s,  
        establish_time= %s,  
        area= %s,  
        mgr_dept= %s,  
        address= %s,  
        doctoral_program_num= %s,  
        master_program_num= %s,  
        important_subject_num= %s,  
        province_id= %s,  
        province_name= %s,  
        city_name= %s,  
        city_id= %s,  
        county_name= %s,  
        county_id= %s,  
        town_name= %s,  
        introduction= %s,  
        f985= %s,  
        f211=%s
        """
        self.cursor.execute(sqlscript,
                            (
                                item['id'],
                                item.get('zh_name', ''),
                                item.get('logo', ''),
                                item.get('official_website', ''),
                                item.get('admissions_contact_phone', ''),
                                item.get('admissions_contact_email', ''),
                                item.get('arwu_ranking', -1),
                                item.get('aa_ranking', -1),
                                item.get('qs_ranking', -1),
                                item.get('usn_ranking', -1),
                                item.get('the_ranking', -1),
                                item.get('edu_level', ''),
                                item.get('edu_category', ''),
                                item.get('edu_establish', ''),
                                item.get('tags', ''),
                                item.get('establish_time', ''),
                                item.get('area', ''),
                                item.get('mgr_dept', ''),
                                item.get('address', ''),
                                item.get('doctoral_program_num', 0),
                                item.get('master_program_num', 0),
                                item.get('important_subject_num', 0),
                                item.get('province_id', 0),
                                item.get('province_name', ''),
                                item.get('city_name', ''),
                                item.get('city_id', 0),
                                item.get('county_name', ''),
                                item.get('county_id', 0),
                                item.get('town_name', ''),
                                item.get('introduction', ''),
                                item.get('f985', 0),
                                item.get('f211', 0),
                                item.get('zh_name', ''),
                                item.get('logo', ''),
                                item.get('official_website', ''),
                                item.get('admissions_contact_phone', ''),
                                item.get('admissions_contact_email', ''),
                                item.get('arwu_ranking', -1),
                                item.get('aa_ranking', -1),
                                item.get('qs_ranking', -1),
                                item.get('usn_ranking', -1),
                                item.get('the_ranking', -1),
                                item.get('edu_level', ''),
                                item.get('edu_category', ''),
                                item.get('edu_establish', ''),
                                item.get('tags', ''),
                                item.get('establish_time', ''),
                                item.get('area', ''),
                                item.get('mgr_dept', ''),
                                item.get('address', ''),
                                item.get('doctoral_program_num', 0),
                                item.get('master_program_num', 0),
                                item.get('important_subject_num', 0),
                                item.get('province_id', 0),
                                item.get('province_name', ''),
                                item.get('city_name', ''),
                                item.get('city_id', 0),
                                item.get('county_name', ''),
                                item.get('county_id', 0),
                                item.get('town_name', ''),
                                item.get('introduction', ''),
                                item.get('f985', 0),
                                item.get('f211', 0),
                            ))

        self.conn.commit()

    def close_spider(self, spider):
        super().close_spider(spider)


class MajorPipeline(Write2DBPipeline):
    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, Major):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        self.data.append((
            item['id'],
            item.get('zh_name', ''),
            item.get('code', ''),
            item.get('edu_level', ''),
            item.get('course_scopes', ''),
            item.get('course_category', ''),
            item.get('edu_duration', ''),
            item.get('graduate', ''),
            item.get('introduction', ''),
            item.get('university_id', '')
        ))
        if len(self.data) > 5:
            self.write_batch_data()
            self.data.clear()

    def write_batch_data(self):
        sqlscript = """
        insert into major(
                  id, 
                  zh_name,
                  code,
                  edu_level,
                  course_scopes,
                  course_category,
                  edu_duration,
                  graduate,
                  introduction,
                  university_id)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on duplicate key update 
            zh_name = values(zh_name),
            code = values(code),
            edu_level =  values(edu_level),
            course_scopes = values(course_scopes),
            course_category = values(course_category),
            edu_duration = values(edu_duration),
            graduate = values(graduate),
            introduction = values(introduction),
            university_id = values(university_id)
        """
        self.cursor.executemany(sqlscript, self.data)
        self.conn.commit()

    def close_spider(self, spider):
        super().close_spider(spider)


class MajorScorePipeline(Write2DBPipeline):

    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, MajorScore):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        self.data.append((
            item.get('str_id'),
            item.get('subject_name'),
            item.get('avg'),
            item.get('max'),
            item.get('min'),
            item.get('min_ranking'),
            item.get('batch_num_name'),
            item.get('subject_scopes_name'),
            item.get('subject_category_name'),
            item.get('major_id'),
            item.get('university_id'),
            item.get('year'),
            item.get('province_id'),
            item.get('province_name'),
            item.get('min_range'),
            item.get('min_rank_range'),
        ))
        if len(self.data) >= 1:
            self.write_batch_data()
            self.data.clear()

    def write_batch_data(self):
        sqlscript = """
                insert into major_score(str_id,
                 subject_name, `avg`, `max`, `min`, min_ranking, 
                 batch_num_name, subject_scopes_name,
                                subject_category_name,
                                 major_id, university_id, `year`, province_id, province_name,
                                 min_range,min_rank_range )
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                on duplicate key update
               `subject_name` = values(`subject_name`),
               `avg` = values(`avg`),
               `max` = values(`max`),
               `min` = values(`min`),
               `min_ranking` = values(`min_ranking`),
               `batch_num_name` = values(`batch_num_name`),
               `subject_scopes_name` = values(`subject_scopes_name`),
               `subject_category_name` = values(`subject_category_name`),
               `min_range` = values(`min_range`),
               `min_rank_range` = values(`min_rank_range`)
                """
        self.cursor.executemany(sqlscript, self.data)
        self.conn.commit()

    def close_spider(self, spider):
        super().close_spider(spider)


class AdmissionsPlanPipeline(Write2DBPipeline):
    def close_spider(self, spider):
        super().close_spider(spider)

    def write_batch_data(self):
        sqlscript = """
        insert into admissions_plan(
        major_name, 
        admissions_stu_num, edu_fee, university_id, 
        major_code, batch_num_name,
        subject_name, `year`,
        province_id, province_name, cond, edu_dur)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        on duplicate key update 
        major_name = values(major_name),
        admissions_stu_num = values(admissions_stu_num),
        edu_fee = values(edu_fee),
        university_id = values(university_id),
        major_code = values(major_code),
        batch_num_name = values(batch_num_name),
        subject_name = values(subject_name),
        `year` = values(`year`),
        `province_id` = values(`province_id`),
        `province_name` = values(`province_name`),
        `cond` = values(`cond`),
        `edu_dur` = values(`edu_dur`)
        """
        self.cursor.executemany(sqlscript, self.data)
        self.conn.commit()

    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, AdmissionsPlan):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        self.data.append((
            item.get('major_name'),
            item.get('admissions_stu_num'),
            item.get('edu_fee'),
            item.get('university_id'),
            item.get('major_code'),
            item.get('batch_num_name'),
            item.get('subject_name'),
            item.get('year'),
            item.get('province_id'),
            item.get('province_name'),
            item.get('cond'),
            item.get('edu_dur'),
        ))
        if len(self.data) >= 10:
            self.write_batch_data()
            self.data.clear()


class AdmissionsNewsPipeline(Write2DBPipeline):
    def close_spider(self, spider):
        super().close_spider(spider)

    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, AdmissionsNews):
            return self._process_item(item, spider)
        return item

    def write_batch_data(self):
        sqlscript = """
        insert into admissions_news(
        id, publish_date, title, content, type_id, type_name, university_id)
        values(%s,%s,%s,%s,%s,%s,%s)
        on duplicate key update 
        publish_date = values(publish_date),
        title = values(title),
        content = values(content),
        type_id = values(type_id),
        type_name = values(type_name),
        university_id = values(university_id)
        """
        self.cursor.executemany(sqlscript, self.data)
        self.conn.commit()

    def _process_item(self, item: scrapy.Item, spider):
        self.data.append((
            item.get('id'),
            item.get('publish_date'),
            item.get('title'),
            item.get('content'),
            item.get('type_id'),
            item.get('type_name'),
            item.get('university_id'),
        ))
        if len(self.data) > 10:
            self.write_batch_data()
            self.data.clear()


class UniversityScorePipeline(Write2DBPipeline):
    def close_spider(self, spider):
        super().close_spider(spider)

    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, UniversityScore):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        self.data.append((
            item.get('year'),
            item.get('admissions_batch_num'),
            item.get('admissions_type'),
            item.get('min'),
            item.get('min_ranking'),
            item.get('max'),
            item.get('avg'),
            item.get('avg_ranking'),
            item.get('province_id'),
            item.get('province_name'),
            item.get('subject_category'),
            item.get('province_control_score'),
            item.get('university_id'),
            item.get('cond'),
            item.get('major_group_id'),
            item.get('major_group_name'),
        ))
        if len(self.data) >= 1:
            self.write_batch_data()
            self.data.clear()

    def write_batch_data(self):
        sqlscript = """
          insert into university_score(year,
                               admissions_batch_num,
                               admissions_type,
                               min,
                               min_ranking,
                               max,
                               avg,
                               avg_ranking,
                               province_id,
                               province_name,
                               subject_category,
                               province_control_score,
                               university_id,
                               cond,
                               major_group_id,
                               major_group_name)
         values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         on duplicate key update
         `min` = values(`min`),
        `min_ranking` = values(`min_ranking`),
        `max` = values(`max`),
        `avg` = values(`avg`),
        `avg_ranking` = values(`avg_ranking`),
        `province_control_score` = values(`province_control_score`),
        `cond` = values(`cond`),
        `major_group_name` = values(`major_group_name`)
          """
        self.cursor.executemany(sqlscript, self.data)
        self.conn.commit()


class UniversityMetricPipeline(Write2DBPipeline):
    def close_spider(self, spider):
        super().close_spider(spider)

    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, EmploymentRegionRateMetric):
            return self._process_region_metric_item(item)
        elif isinstance(item, CompanyAttrRateMetric):
            return self._process_companyattr_metric_item(item)
        elif isinstance(item, CompanyMetric):
            return self._process_company_metric_item(item)
        return item

    def _process_region_metric_item(self, item: scrapy.Item):
        sqlscript = """
        insert into employment_region_rate_metric(university_id, rate, province_name, `year`) 
        value(%s,%s,%s,%s)
        on duplicate key update 
        rate = values(rate)
        """
        self.cursor.executemany(sqlscript, [
            (
                item.get('university_id'),
                item.get('rate'),
                item.get('province_name'),
                item.get('year'),
            )
        ])
        self.conn.commit()

    def _process_companyattr_metric_item(self, item: scrapy.Item):
        sqlscript = """
        insert into company_attr_rate_metric(university_id, name, rate) 
        VALUES (%s,%s,%s)
        on duplicate key update
        rate = values(rate)
        """
        self.cursor.executemany(sqlscript, [
            (
                item.get('university_id'),
                item.get('name'),
                item.get('rate'),
            )
        ])
        self.conn.commit()

    def _process_company_metric_item(self, item: scrapy.Item):
        sqlscript = """
        insert into company_metric(university_id, name, sort) 
        VALUES (%s,%s,%s)
        on duplicate key update 
        sort = values(sort)
        """
        self.cursor.executemany(sqlscript, [
            (
                item.get('university_id'),
                item.get('name'),
                item.get('sort'),
            )
        ])
        self.conn.commit()


class ErrorResponsePipeline(Write2DBPipeline):
    def close_spider(self, spider):
        super().close_spider(spider)

    def process_item(self, item: scrapy.Item, spider):
        if isinstance(item, ErrorResponse):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        self.data.append((
            item.get('api_name'),
            item.get('ctx_id'),
            item.get('university_id'),
            item.get('url'),
            item.get('method'),
            item.get('ctx_para'),
        ))
        if len(self.data) >= 0:
            self.write_batch_data()
            self.data.clear()

        return item

    def write_batch_data(self):
        sqlscript = """
        insert into error_response(
        api_name, ctx_id, university_id, url, method,ctx_para) 
        values (%s,%s,%s,%s,%s,%s)
        """
        self.cursor.executemany(sqlscript, self.data)
        self.conn.commit()
