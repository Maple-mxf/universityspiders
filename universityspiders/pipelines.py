# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from universityspiders.items import University, Major


class UniversityspidersPipeline:
    def process_item(self, item: scrapy.Item, spider):

        print(item)

        if isinstance(item, University):
            print('University')
        elif isinstance(item, Major):
            print('Major')

        return item
