# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['scomedy.com']
    start_urls = ['http://scomedy.com/quotes']

    def parse(self, response):
        for quote in response.css('div.views-row'):
            item = {
                'comedian': quote.css('a::text')[1].extract(),
                'text': quote.css('p::text').extract(),
                'tags': quote.css('a::text')[2:].extract()
            }
            yield item

        next_page = response.css('li.pager__item--next > a::attr(href)')
        if next_page:
            next_page_url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url=next_page_url, callback=self.parse)
