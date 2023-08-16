from gc import callbacks
import json
import random
from urllib.parse import urlencode
import scrapy
from bookscraper.items import BookItem

# For Generating proxy url with ip and headers (proxy_method_3)
# API_KEY = ''
# def get_proxy_url(url):
#     payload = {'api-key': API_KEY, 'url': url}
#     proxy_url = 'https://proxy.scrapeops.io/v1?' + urlencode(payload)
#     return proxy_url

'''Scrapper spider for target to crawl and extract data'''

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com"]
    
    # data/%(name)s_%(time)s
    custom_settings = {
        'FEED':{
            'booksdata.json': {'format': 'json', 'overwrite': True}
        }
    }
    
    # Get proxy url for the fist endpoint (proxy_method_3)
    # def start_requests(self):
    #     yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)
    

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            # (proxy_method_1)
            yield response.follow(book_url, callback=self.parse_book_page) 
            # (proxy_method_2)
            # yield response.follow(book_url, callback=self.parse_book_page, meta={"proxy": "user-asds3a4545:12345678@gate.smartproxy.com:7000"}) 
            # (proxy_method_3)
            # yield response.follow(get_proxy_url(book_url), callback=self.parse_book_page) 
            
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            # (proxy_method_1)
            yield response.follow(next_page_url, callback=self.parse) 
            # (proxy_method_2)
            # yield response.follow(next_page_url, callback=self.parse, meta={"proxy": "user-asds3a4545:12345678@gate.smartproxy.com:7000"}) 
            # (proxy_method_3)
            # yield response.follow(get_proxy_url(next_page_url), callback=self.parse) 

    
    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        book_item = BookItem()
    
        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['upc'] = table_rows[0].css('td ::text').get()
        book_item['product_type'] = table_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        book_item['tax'] = table_rows[4].css('td ::text').get()
        book_item['availibility'] = table_rows[5].css('td ::text').get()
        book_item['num_reviews'] = table_rows[6].css('td ::text').get()
        book_item['stars'] = response.css('p.star-rating').attrib['class']
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = response.css('p.price_color ::text').get()
        book_item['image'] = response.css('div.item img ::attr(src)').get()
    
        yield book_item
