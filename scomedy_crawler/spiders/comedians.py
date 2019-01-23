# -*- coding: utf-8 -*-
import scrapy


class ComediansSpider(scrapy.Spider):
    name = 'comedians'
    allowed_domains = ['scomedy.com']
    start_urls = ['http://scomedy.com/comedians']

    def parse(self, response):
        comedians = response.css('div.view-comedians')
        comedians_url = comedians.css('a::attr(href)').extract()
        for comedian_url in comedians_url:
            url = response.urljoin(comedian_url)
            yield scrapy.Request(url=url, callback=self.parse_comedian)

    def parse_comedian(self, response):
        comedian = response.css('h1.page-title > span::text').extract_first()
        full_name = response.css('div.field--name-field-full-name')
        full_name = full_name.css('div.field__item::text').extract_first()
        country = response.css('div.field--name-field-country')
        country = country.css('div.field__item::text').extract_first()
        bio = response.css('p::text').extract_first()

        item = {
            'comedian': comedian,
            'full_name': full_name,
            'country': country,
            'bio': bio
        }
        yield item
