import scrapy

# scrape links to laptops using links from pages.csv

# crate a field for the links
class Link(scrapy.Item):
    link = scrapy.Field()

# create a spider to scrape the links
class LaptopsSpider(scrapy.Spider):
    name = 'laptops_links'
    allowed_domains = ['https://www.euro.com.pl/']
   
    # use pages.csv from pages.py
    try:
        with open("pages.csv", "rt") as f:
            start_urls = [url.strip('""\n') for url in f.readlines()][1:]
    except:
        start_urls = []

    # create a file with links to laptops
    def parse(self, response):
        xpath = '//div[@class="product-row"]//a[@class="js-save-keyword"]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.euro.com.pl/' + s.get()
            yield l
