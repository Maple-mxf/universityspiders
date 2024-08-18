import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from universityspiders.items import (
    University,
    Major,
    MajorScore,
    AdmissionsPlan
)
import pymysql
import re
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

                                # =====>
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
            item['str_id'],
            item['subject_name'],
            item['avg'],
            item['max'],
            item['min'],
            item['min_ranking'],
            item['batch_num_name'],
            item['subject_scopes_name'],
            item['subject_category_name'],
            item['major_id'],
            item['university_id'],
            item['year'],
            item['province_id'],
            item['province_name'],
            item['min_range'],
            item['min_rank_range'],
        ))
        if len(self.data) >= 10:
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
        subject_name=values(subject_name),
        `avg`=values(`avg`),
        `max`=values(`max`),
        `min`=values(`min`),
        min_ranking=values(min_ranking),
        batch_num_name=values(batch_num_name),
        subject_scopes_name=values(subject_scopes_name),
        subject_category_name=values(subject_category_name),
        major_id=values(major_id),
        university_id=values(university_id),
        `year`=values(`year`),
        province_id=values(province_id),
        province_name=values(province_name),
        min_range=values(min_range),
        min_rank_range=values(min_rank_range)
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
            item['major_name'],
            item['admissions_stu_num'],
            item['edu_fee'],
            item['university_id'],
            item['major_code'],
            item['batch_num_name'],
            item['subject_name'],
            item['year'],
            item['province_id'],
            item['province_name'],
            item['cond'],
            item['edu_dur'],
        ))
        if len(self.data) >= 10:
            self.write_batch_data()
            self.data.clear()
