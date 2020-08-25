# -*- coding: utf-8 -*-
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'AgusSpider'
    download_delay = 1.0
    start_urls = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=watches&_sacat=0&_ipg=200'
    items_crawled = {}

    def start_requests(self):
        yield scrapy.Request(self.start_urls, callback=self.parse)

    def parseOwner(self, response):
        item_data = response.meta.get('item_data')
        owner_data = response.meta.get('owner_data')
        owner_score = response.css('#user_info div.perctg ::text').get()
        
        yield {'item': item_data, 'owner': owner_data, 'score': owner_score}


    def parseWatch(self, response):
        item_data = response.meta.get('item_data')
        owner = response.css('#mbgLink')
        owner_link = owner.css('::attr(href)').get()
        owner_data = owner.css('span ::text').get()
        
        yield scrapy.Request(owner_link, callback=self.parseOwner, meta={'item_data': item_data, 'owner_data': owner_data})


    def parse(self, response):
        items = response.css('a.s-item__link')

        for item in items:

            item_link = item.css('::attr(href)').get()
            item_data = item.css('h3 ::text').get()

            if item_link and item_link not in self.items_crawled:
                self.items_crawled[item_link] = 1
            
                yield scrapy.Request(item_link, callback=self.parseWatch, meta={'item_data': item_data})


