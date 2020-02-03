# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
import random
from scrapy import Request
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from zhihu_spider.misc.tools import get_ua_list

"""
遇到验证码检测重试
"""


class ZhihuRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if 'account/unhuman' in response.url:
            reason = 'zhihu need login %s' % request
            return self._retry(request, reason, spider)
        return response


"""
此处需要自行设定代理
"""


class MyproxiesSpiderMiddleware(object):

    count = 0

    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        with open('zhihu_spider/txt/ip_list.txt', 'r') as f:
            line = f.read().strip()
            linestr = line.split('\n')
        thisip = linestr[self.count % 1500]
        self.count += 1
        print("this is ip: " + thisip)
        request.meta["proxy"] = "http://" + thisip


class ZhihuDownloaderMiddleware(object):
    '''
    下载器中间件
    '''

    def process_request(self, request: Request, spider):
        request.headers['User-Agent'] = random.choice(get_ua_list())
