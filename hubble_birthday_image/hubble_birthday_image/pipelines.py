# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class HubbleBirthdayImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """Override get_media_requests to pass in meta"""
        for image_url in item["image_urls"]:
            yield scrapy.Request(image_url, meta={"path": item["name"]})

    def get_custom_path(self, response):
        """Get custom path based `path` in response.meta"""
        return f'full/{response.meta["path"]}'

    def get_images(self, response, request, info):
        """Override get_images to use custom path"""
        for path, image, buf in super().get_images(response, request, info):
            path = self.get_custom_path(response)
        yield path, image, buf
