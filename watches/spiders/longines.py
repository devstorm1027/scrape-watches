from __future__ import division, absolute_import, unicode_literals

import re
import scrapy
import json
import traceback
from scrapy.http import Request
from watches.items import WatchesItem


class LonginesProductsSpider(scrapy.Spider):
    name = 'longines_products'
    allowed_domains = ["www.longines.com"]
    START_URL = 'https://www.longines.com/retailers/gb'

    def start_requests(self):
        yield Request(
            url=self.START_URL,
            callback=self.parse_product,
            dont_filter=True
        )

    def parse_product(self, response):
        product = WatchesItem()

        json_data = []
        try:
            json_data = json.loads(re.search('retailersJSON =(.*?);', response.body).group(1))
        except:
            self.log("Error to parse json data".format(traceback.format_exc()))

        for data in json_data:
            retailer = data.get('name')
            product['retailer'] = retailer

            store_name = retailer
            product['store_name'] = store_name

            address = data.get('address')
            zipcode = data.get('zipcode')
            city = data.get('city')
            full_address = ' '.join([address, zipcode, city])
            product['address'] = full_address

            email = data.get('email')
            product['email'] = email

            phone = data.get('phone')
            product['phone'] = phone

            product['stock'] = False

            yield product