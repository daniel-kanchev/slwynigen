import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from slwynigen.items import Article


class SlwynigenSpider(scrapy.Spider):
    name = 'slwynigen'
    start_urls = ['https://www.slwynigen.ch/aktuelles/']

    def parse(self, response):
        links = response.xpath('//h2/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        content = response.xpath('//div[@class="csc-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        title = content.pop(0).strip()
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
