# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from universityspiders.items import University, Major
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

    def write_restdata_batch(self):
        pass

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.write_restdata_batch()
            self.conn.commit()
        self.conn.close()
        pass


class UniversityPipeline(Write2DBPipeline):
    def process_item(self, item: scrapy.Item, spider):
        print(item)
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
        pass
