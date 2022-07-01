from bs4 import BeautifulSoup
import requests
import re
import logging as log

def search():
    log.info('Scraping dw.com')
    r = requests.get('https://www.dw.com/en')
    site = BeautifulSoup(r.text, 'html.parser')

    carousels = site.find_all('div', 'carouselTeaser')

    search = ''
    if len(carousels) > 0:
        carousel = carousels[0]
        featured_article = carousel.find('h2')

        words = featured_article.string.split()

        if len(words) > 0:
            search = re.sub('[^A-Za-z0-9 ]+', '', words[0].lower())

        log.info('Main topic found is: %s' % search)

    return search
