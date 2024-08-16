import time

import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse, TextResponse
from itemadapter import is_item, ItemAdapter
from selenium.webdriver.common.by import By

from universityspiders.spiders.university import UniversitySpider


class UniversityspidersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class UniversityspidersDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: scrapy.Request, spider: UniversitySpider):
        time.sleep(2)
        cb_kwargs: dict = request.cb_kwargs
        if cb_kwargs.get('api', None) is not None:
            if request.method == 'GET':
                spider.driver.get(request.url)
                content = spider.driver.find_element(By.TAG_NAME, 'pre').text
                return TextResponse(url=request.url, request=request, body=content, encoding='utf-8')
            else:
                # spider.driver.execute_script()
                print('暂时不支持POST请求')
        else:
            spider.driver.get(request.url)
            html = spider.driver.page_source
            return HtmlResponse(url=request.url, request=request, body=html, encoding='utf-8')

    def process_response(self, request, response: scrapy.http.TextResponse, spider):
        return response

    def process_exception(self, request: scrapy.Request, exception, spider):
        print(f'Exception[url={request.url}, method={request.method}, cb_kwargs={request.cb_kwargs}]')

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
