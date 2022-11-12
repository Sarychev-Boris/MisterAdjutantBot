import scrapy
import os


class DaySpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['kakoysegodnyaprazdnik.ru']
    start_urls = ['http://kakoysegodnyaprazdnik.ru/']
    global PATH
    PATH = os.path.abspath(os.curdir)  

    def parse(self, response):
        with open(PATH + '/data/events.txt', 'w', encoding='utf-8') as file:

            file.write(response.css('h2.mainpage::text').get())
            print(response.css('h2.mainpage::text').get())
            file.write('\n\n')

            for event in response.css('span[itemprop*=text]::text').getall():
                file.write(f'• {event} \n')

            file.write('\nСОБЫТИЯ В ИСТОРИИ\n\n')

            for event in response.css('div.event::text').getall():
                file.write(f'{event} \n')
