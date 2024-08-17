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
                match line:
                    case str(x) if '官方网址' in x:
                        item['official_website'] = x
                    case str(x) if '招生电话' in x:
                        item['admission_contact_phone'] = x
                    case str(x) if '电子邮箱' in x:
                        item['admission_contact_email'] = x

        baseinfo2 = item.get('baseinfo2', None)
        if baseinfo2 is not None:
            for line in baseinfo2:
                matcher = re.match('^(\d+)(.*)$', line)
                if matcher:
                    num = matcher.group(1)
                    desc = matcher.group(2)
                    match desc:
                        case str(x) if '博士点' in x:
                            item['doctoral_program_num'] = num
                        case str(x) if '硕士点' in x:
                            item['master_program_num'] = num
                        case str(x) if '国家重点学科' in x:
                            item['important_score_num'] = num

        baseinfo3 = item.get('baseinfo3', None)
        if baseinfo3 is not None:
            item['tags'] = [x for x in baseinfo3]


        return item

    def _execute_sqlscript(self, item):
        pass

    def close_spider(self, spider):
        pass
