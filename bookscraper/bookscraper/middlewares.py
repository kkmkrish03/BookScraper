# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from email.mime import base
from struct import pack
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BookscraperSpiderMiddleware:
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


class BookscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        

from urllib.parse import urlencode
from random import randint
import requests

class ScrapeOpsFakeUserAgentMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings) -> None:
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'https://headers.scrapeops.io/v1/user-agents')
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.user_agent_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()
        
    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agent_list = json_response.get('result', [])
        
    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agent_list) - 1)
        return self.user_agent_list[random_index]
    
    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True
            
    def process_request(self, request, spider):
        if self.scrapeops_fake_user_agents_active:  
            random_user_agent = self._get_random_user_agent()
            request.headers['User-Agent'] = random_user_agent
            print('**************** NEW HEADER ATTACHED ****************')
            print(request.headers['User-Agent'])
        



class ScrapeOpsFakeBrowserHeaderAgentMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings) -> None:
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'https://headers.scrapeops.io/v1/browser-headers')
        self.scrapeops_fake_browser_header_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.browser_header_list = []
        self._get_browser_header_list()
        self._scrapeops_fake_browser_header_enabled()
        
    def _get_browser_header_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.browser_header_list = json_response.get('result', [])
        
    def _get_random_browser_header(self):
        random_index = randint(0, len(self.browser_header_list) - 1)
        return self.browser_header_list[random_index]
    
    def _scrapeops_fake_browser_header_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_header_active == False:
            self.scrapeops_fake_browser_header_active = False
        else:
            self.scrapeops_fake_browser_header_active = True
            
    def process_request(self, request, spider):
        if self.scrapeops_fake_browser_header_active:
            random_browser_header = self._get_random_browser_header()
            request.headers['accept-language'] = random_browser_header['accept-language']
            request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user'] 
            request.headers['sec-fetch-mod'] = random_browser_header['sec-fetch-mod']
            request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
            request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform']
            request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile']
            request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua']
            request.headers['accept'] = random_browser_header['accept']
            request.headers['user-agent'] = random_browser_header['user-agent']
            request.headers['upgrade-insecure-requests'] = random_browser_header['upgrade-insecure-requests']
            print('**************** NEW HEADER ATTACHED ****************')
            print(request.headers)
        

import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

class MyFreeProxyMiddleware(HttpProxyMiddleware):
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings) -> None:
        self.proxy_list_by = settings.get('PROXYLIST_BY', 'SPEED')
        match self.proxy_list_by:
            case 'SPEED': self.proxy_list_endpoint = settings.get('ROTATING_PROXYLIST_ENDPOINT_BY_SPEED')
            case 'UPTIME': self.proxy_list_endpoint = settings.get('ROTATING_PROXYLIST_ENDPOINT_BY_UP_TIME')
            case 'RESPONSE': self.proxy_list_endpoint = settings.get('ROTATING_PROXYLIST_ENDPOINT_BY_RESPONSE')
            case _ : self.proxy_list_endpoint = settings.get('ROTATING_PROXYLIST_ENDPOINT_BY_SPEED')
        self.proxy_list_enabled = settings.get('PROXYLIST_ENABLED', False)
        self.proxy_list = []
        self.current_proxy = None
        self._get_proxy_list()
        self._proxy_list_enabled()
    
    def _proxy_list_enabled(self):
        if self.proxy_list_endpoint is None or self.proxy_list_endpoint == '' or self.proxy_list_enabled == False or len(self.proxy_list)<1:
            self.proxy_list_enabled = False
        else:
            self.proxy_list_enabled = True
    
    def _get_proxy_list(self):
        response = requests.get(self.proxy_list_endpoint)
        print(response.json())
        json_response = response.json()
        self.proxy_list = json_response.get('data', [])
        
    def _set_proxy(self, request, scheme):
        if not self.current_proxy or self.current_proxy not in self.proxy_list:
            random_index = randint(0, len(self.proxy_list) - 1)
            self.current_proxy = self.proxy_list[random_index]
            # self.current_proxy = random.choice(self.proxy_list)
            request.meta['proxy'] = f'{scheme}://{self.current_proxy["ip"]}:{self.current_proxy["port"]}'
            print('**************** NEW PROXY URL ****************')
            print(f'{scheme}://{self.current_proxy["ip"]}:{self.current_proxy["port"]}')
        
    def process_request(self, request, spider):
        if self.proxy_list_enabled:
            scheme = 'http' if 'http://' in request.url else 'https'
            self._set_proxy(request, scheme)
            super().process_request(request, spider)
        
                
import base64
class MyProxyMiddleware(object):
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings) -> None:
        self.user = settings.get('PROXY_USER')
        self.password = settings.get('PROXY_PASSWORD')
        self.endpoint = settings.get('PROXY_ENDPOINT')
        self.port = settings.get('PROXY_PORT')
        
    def process_request(self, request, spider):
        user_credentials = f'{self.user}:{self.password}'
        basic_authentication = 'Basic ' + base64.b64encode(user_credentials.encode()).decode()
        host = f'http://{self.endpoint}:{self.port}'
        request.meta['proxy'] = host
        request.headers['Proxy-Authentication'] = basic_authentication
        print('**************** NEW HEADER ATTACHED ****************')
        print(request.headers['User-Agent'])