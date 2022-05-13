import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LaptopsSpider(scrapy.Spider):
    name = 'laptops'
    allowed_domains = ['https://www.euro.com.pl/']
    try:
        with open("pages.csv", "rt") as f:
            start_urls = [url.strip('""\n') for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        print(response)
        xpath = '//div[@class="product-row"]//a[@class="js-save-keyword"]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.euro.com.pl/' + s.get()
            yield l
