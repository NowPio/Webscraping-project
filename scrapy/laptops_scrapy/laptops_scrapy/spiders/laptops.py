import scrapy


# limit the number of scraped laptops to 100
limit_100 = True

# define product details that will be scraped
class Laptop(scrapy.Item):
    brand = scrapy.Field()
    price = scrapy.Field()
    screen = scrapy.Field()
    battery = scrapy.Field()
    processor = scrapy.Field()
    RAM = scrapy.Field()
    ssd_memory = scrapy.Field()
    graphic_card = scrapy.Field()
    laptop_type = scrapy.Field()
    system = scrapy.Field()
    
class LaptopSpider(scrapy.Spider):
    name = 'laptops'
    allowed_domains = ['https://www.euro.com.pl/']
    try:
        with open("laptops.csv", "rt") as f:
            start_urls = [url.strip('""\n') for url in f.readlines()][1:]
    except:
        start_urls = []
    
    # limit the number of the urls to be scraped to 100
    if limit_100 == True:
        start_urls = start_urls[0:100]	
	
    def parse(self, response):
        l = Laptop()
        
        # define xpaths to product details
        brand_xpath = 'normalize-space(//li[contains(text(), "Marka:")]/span/text())'
        price_xpath = 'normalize-space(//div[@class="product-price"]/@data-price)'
        screen_xpath = 'normalize-space(//a[normalize-space()="Ekran"]/following::td[1]/text())'
        battery_xpath = 'normalize-space(//a[normalize-space()="Pojemność baterii/akumulatora"]/following::td[1]/text())'
        processor_xpath = 'normalize-space(//a[normalize-space()="Model procesora"]/following::td[1]/text())'
        RAM_xpath = 'normalize-space(//a[normalize-space()="Pamięć RAM"]/following::td[1]/text())'
        ssd_memory_xpath = 'normalize-space(//a[normalize-space()="Szybki dysk SSD"]/following::td[1]/text())'
        graphic_card_xpath = 'normalize-space(//a[normalize-space()="Model karty graficznej"]/following::td[1]/text())'
        laptop_type_xpath = 'normalize-space(//a[normalize-space()="Typ"]/following::td[1]/text())'
        system_xpath = 'normalize-space(//td[contains(text(), "System operacyjny")]/following::td[1])'
        
        # fetch data
        l['brand'] = response.xpath(brand_xpath).getall()
        l['price'] = response.xpath(price_xpath).getall()
        l['screen'] = response.xpath(screen_xpath).getall()
        l['battery'] = response.xpath(battery_xpath).getall()
        l['processor'] = response.xpath(processor_xpath).getall()
        l['RAM'] = response.xpath(RAM_xpath).getall()
        l['ssd_memory'] = response.xpath(ssd_memory_xpath).getall()
        l['graphic_card'] = response.xpath(graphic_card_xpath).getall()
        l['laptop_type'] = response.xpath(laptop_type_xpath).getall()
        l['system'] = response.xpath(system_xpath).getall()
        
        yield l
    
  