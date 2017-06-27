# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem

# name, allowed_domains, start_urls, parse attributes are required.
class DmozSpiderSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoztools.net"]
    start_urls = ['http://dmoztools.net/Computers/Programming/Languages/Python/Books/',
                  'http://dmoztools.net/Computers/Programming/Languages/Python/Resources/']

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        for sel in response.xpath('//*[@id="site-list-content"]/div/div[3]'):
            item = TutorialItem()
            item['name'] = sel.xpath('a/div/text()').extract()[0]
            item['link'] = sel.xpath('a/@href').extract()[0]
            item['desc'] = sel.xpath('div/text()').extract()[0].strip()
            yield item

