import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('//span[@class="text"]/text()').get(),
                'author': quote.xpath('//small[@class="author"]/text()').get(),
                'tags': quote.xpath('//div[@class="tags"]//a[@class="tag"]/text()').getall()
            }

        next_page=response.css('li.next a::attr(href)').get()
        if next_page :
            yield response.follow(next_page,callback=self.parse)