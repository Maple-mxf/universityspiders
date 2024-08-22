from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    restore = os.environ.get('SPIDER_RESTORE', 'F')
    ctx_id = os.environ.get('SPIDER_CTX_ID', None)

    execute([
        'scrapy',
        'crawl',
        'university',
        '-a',
        f'restore={restore}',
        '-a',
        f'ctx_id={ctx_id}'
    ])
