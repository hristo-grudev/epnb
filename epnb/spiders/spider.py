import scrapy

from scrapy.loader import ItemLoader

from ..items import EpnbItem
from itemloaders.processors import TakeFirst


class EpnbSpider(scrapy.Spider):
	name = 'epnb'
	start_urls = ['https://www.epnb.com/insights/category/enb-news/']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space() and not(ancestor::div[@class="date"] | ancestor::a)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date"]/text()').get()

		item = ItemLoader(item=EpnbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
