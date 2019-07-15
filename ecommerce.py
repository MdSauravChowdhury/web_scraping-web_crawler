# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

'''
def pro_des(response, value):
	return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()
'''

def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()


class EcommerceSpider(scrapy.Spider):
    name = 'ecommerce'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']


    def parse(self, response):
        selector = response.xpath("//h3/a/@href").extract()

        for join in selector:
        	absoulate_url = response.urljoin(join)

        	yield Request(absoulate_url, callback=self.parse_item)

        # Next Page Url	
        absoulate_url = response.xpath("//a[text()='next']/@href").extract_first()
        next_page_url = response.urljoin(absoulate_url)

        yield Request(next_page_url)

    def parse_item(self, response):

    	title = response.xpath("//h1/text()").extract_first()
    	price = response.xpath(".//*[@class='price_color']/text()").extract_first()
    	rating = response.xpath("//*[contains(@class, 'star-rating')]/@class").extract_first()
    	rating = rating.replace("star-rating", '')
    	pro_des = response.xpath('//*[@id="content_inner"]/article/p/text()').extract()
    	
    	# Product Information
    	upc = product_info(response, 'UPC')	
    	pro_type = product_info(response, 'Product Type')
    	price_tax = product_info(response, 'Price (excl. tax)')
    	price_incl = product_info(response, 'Price (incl. tax)')
    	tax = product_info(response, 'Tax')
    	avail = product_info(response, 'Availability')
    	review = product_info(response, 'Number of reviews')

    
    	yield {
    		'BOOK_TITLE':title,
    		'BOOK_PRICE':price,
    		'RATING':rating,

    		'UPC':upc,
    		'PRODUCT TYPE':pro_type,
    		'Price (excl. tax)':price_tax,
    		'Price (incl. tax)':price_incl,
    		'Tax':tax,
    		'Availability':avail,
    		'Number of reviews':review
    	}