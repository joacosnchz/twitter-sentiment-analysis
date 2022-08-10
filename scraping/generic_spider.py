import os
import re
import scrapy
import logging as log

class GenericSpider(scrapy.Spider):
    name = 'genericspider'
    start_urls = os.getenv('URLS').split(' ')

    def parse(self, response):
        if 'https://www.dw.com/en' in response.url:
            log.info('Scraping dw.com...')

            search = ''

            carousels = response.css('div.carouselTeaser')
            if len(carousels) > 0:
                carousel = carousels[0]
                featured_article = carousel.css('h2::text').get()

                words = featured_article.split()

                if len(words) > 0:
                    search = re.sub('[^A-Za-z0-9 ]+', '', words[0].lower())

                log.info('Main topic: %s' % search)
            
            return {'search': search}
