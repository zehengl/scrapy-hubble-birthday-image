import os
from urllib.parse import urlparse

import scrapy
from ..items import HubbleBirthdayImageItem


class ImageSpider(scrapy.Spider):
    base = "https://imagine.gsfc.nasa.gov/hst_bday/images/"
    name = "images"
    start_urls = [base]

    def parse(self, response):
        hrefs = response.xpath("/html/body/pre/a/@href").extract()
        items = [
            HubbleBirthdayImageItem(
                image_urls=[self.get_url(href)], name=self.get_name(href)
            )
            for href in hrefs[5:]
        ]
        yield from items

    def get_name(self, href):
        mapping = {
            "april": "04",
            "august": "08",
            "december": "12",
            "february": "02",
            "january": "01",
            "july": "07",
            "june": "06",
            "march": "03",
            "may": "05",
            "november": "11",
            "october": "10",
            "september": "09",
        }
        segments = href.split("-")
        month = segments.pop(0)
        day = segments.pop(0)
        year = segments.pop(0)

        month = mapping[month]
        day = day.zfill(2)

        segments = [year, month, day] + segments

        return ("-").join(segments)

    def get_url(self, href):
        return f"{self.base}{href}"
