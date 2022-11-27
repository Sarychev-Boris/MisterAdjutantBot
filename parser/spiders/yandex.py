import scrapy
from scrapy.http import Request
from fake_useragent import UserAgent
import urllib
import os
import json
import random
from scrapy.exceptions import CloseSpider


class YandexSpider(scrapy.Spider):
    name = 'yandex'
    allowed_domains = ['yandex.ru']
    global PATH
    PATH = os.path.abspath(os.curdir)

    try:
        with open(PATH + '/data/events.txt', encoding='utf-8') as file:
            event = file.readlines()[2:3][0].strip().strip('• ')
            a = event.count(' ')
            event = event.replace(' ', '+', a)
    except FileNotFoundError:
        pass
    global start_urls
    start_urls = [f'https://yandex.ru/images/search?text={event}']
    # start_urls = ['yandex.ru']

    def start_requests(self):
        with open(PATH + '/data/proxy.json') as file:

            data = [ip for ip in json.load(file).keys()]

            proxy = random.choice(data)
            print('####')    
            print(proxy)
            print('####')  
        yield Request(url=start_urls[0], callback=self.parse,
                      headers={"User-Agent": UserAgent().random},
                      meta={"proxy": proxy, 'max_retry_times': 3, 'handle_httpstatus_all': True, 'download_timeout': 10})

    def parse(self, response):
        src = response.css('img.serp-item__thumb::attr(src)').get()
        urllib.request.urlretrieve('https:' + src, PATH + "/data/image/postcard.png")
