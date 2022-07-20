FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY custom_settings.py .

RUN pip install -r requirements.txt \
    && scrapy startproject scraping \
    && cat scraping/scraping/settings.py >> custom_settings.py \
    && mv custom_settings.py scraping/scraping/settings.py

WORKDIR scraping

COPY proxy_middleware.py scraping
COPY file_pipeline.py scraping
COPY generic_spider.py scraping/spiders

ENTRYPOINT ["scrapy", "crawl", "genericspider"]
