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


class UniversityPipeline(Write2DBPipeline):
    def process_item(self, item: scrapy.Item, spider):
        print(item)
        if isinstance(item, University):
            return self._process_item(item, spider)
        return item

    def _process_item(self, item: scrapy.Item, spider):
        baseinfo1 = item.get('baseinfo1', None)
        if baseinfo1 is not None:
            for line in baseinfo1:
                if '官方网址' in line:
                    item['official_website'] = line
                elif '招生电话' in line:
                    item['admission_contact_phone'] = line
                elif '电子邮箱' in line:
                    item['admission_contact_email'] = line

        baseinfo2 = item.get('baseinfo2', None)
        if baseinfo2 is not None:
            for line in baseinfo2:
                matcher = re.match('^(\d+)(.*)$', line)
                if matcher:
                    num = matcher.group(1)
                    desc = matcher.group(2)
                    if '博士点' in desc:
                        item['doctoral_program_num'] = num
                    elif '硕士点' in desc:
                        item['master_program_num'] = num
                    elif '国家重点学科' in desc:
                        item['important_score_num'] = num

        baseinfo3 = item.get('baseinfo3', None)
        if baseinfo3:
            item['tags'] = [x for x in baseinfo3]

        baseinfo4 = item.get('baseinfo4', None)
        if baseinfo4:
            for line in baseinfo4:
                matcher1 = re.match('^\\s*建校时间：\\s*(\\d+)(.*)\\s*$', line)
                if matcher1:
                    item['establish_time'] = matcher1.group(1)
                matcher2 = re.match('^\\s*占地面积：\\s*(\\d+[\u4e00-\u9fa5]*)\\s*$', line)
                if matcher2:
                    item['area'] = matcher2.group(1)
                matcher3 = re.match('^\\s*主管部门：\\s*(.*)\\s*$', line)
                if matcher3:
                    item['mgr_dept'] = matcher3.group(1)
                matcher4 = re.match('^\\s*学校地址：\\s*(.*)\\s*$', line)
                if matcher4:
                    item['address'] = matcher4.group(1)

        baseinfo5 = item.get('baseinfo5', None)
        if baseinfo5:
            for line in baseinfo5:
                matcher1 = re.match('^.*博士\\D+(\\d+)\\D+$', line)
                if matcher1:
                    item['doctoral_program_num'] = matcher1.group(1)
                matcher2 = re.match('^.*硕士\\D+(\\d+)\\D+$', line)
                if matcher2:
                    item['master_program_num'] = matcher2.group(1)
                matcher3 = re.match('^.*国家重点学科\\D+(\\d+)\\D+$', line)
                if matcher3:
                    item['important_score_num'] = matcher3.group(1)




        return item

    def _execute_sqlscript(self, item):
        pass

    def close_spider(self, spider):
        pass
