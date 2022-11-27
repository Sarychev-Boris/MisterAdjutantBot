import scrapy
import json
import os

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['http://free-proxy-list.net/']
    global PATH
    PATH = os.path.abspath(os.curdir)


    def parse(self, response):
        with open(PATH + '/data/proxy.json') as file:

            data = json.load(file)

            keys = response.css('table.table-striped').css('th::text').getall()
            for tr in response.css('table.table-striped').css('tbody').css('tr'):
                values = tr.css('td::text').getall()
                # To get ip with 80/8080 port and https, which works with hight probability
                if values[1] == '80' and values[6] == 'yes' and values[4] == 'elite proxy' or values[1] == '8080' and values[6] == 'yes' and values[4] == 'elite proxy':
                    data.setdefault(f'http://{values[0]}:{values[1]}', values[3])
                    #data["proxy_list"].append({key: value for key, value in zip(keys, values)})
            with open(PATH + '/data/proxy.json', 'w') as file:
                json.dump(data, file)
 



