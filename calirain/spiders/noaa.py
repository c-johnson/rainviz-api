# -*- coding: utf-8 -*-
import scrapy


class NoaaSpider(scrapy.Spider):
    name = "noaa"
    allowed_domains = ["www.cnrfc.noaa.gov"]
    start_urls = (
        'http://www.www.cnrfc.noaa.gov/',
    )

    def parse(self, response):
        pass
