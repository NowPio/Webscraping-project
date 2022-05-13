import scrapy

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
    case = scrapy.Field()
    system = scrapy.Field()
    
class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    allowed_domains = ['https://www.euro.com.pl/']
    try:
        with open("laptops.csv", "rt") as f:
            start_urls = [url.strip('""\n') for url in f.readlines()][1:]
    except:
        start_urls = []
    
    def parse(self, response):
        l = Laptop()
        
        brand_xpath = '//li[contains(text(), "Marka:")]/span/text()'
        price_xpath = '//div[@class="product-price selenium-price-normal"]/text()'
        screen_xpath = '//a[normalize-space()="Ekran"]/following::td[1]/text()'
        battery_xpath = '//a[normalize-space()="Pojemność baterii/akumulatora"]/following::td[1]/text()'
        processor_xpath = '//a[normalize-space()="Model procesora"]/following::td[1]/text()'
        RAM_xpath = '//a[normalize-space()="Pamięć RAM"]/following::td[1]/text()'
        ssd_memory_xpath = '//a[normalize-space()="Szybki dysk SSD"]/following::td[1]/text()'
        graphic_card_xpath = '//a[normalize-space()="Model karty graficznej"]/following::td[1]/text()'
        laptop_type_xpath = '//a[normalize-space()="Typ"]/following::td[1]/text()'
        case_xpath = '//a[normalize-space()="Materiał obudowy"]/following::td[1]/text()'
        system_xpath = '//td[contains(text(), "System operacyjny")]/following::td[1]/text()'
        
        l['brand'] = response.xpath(brand_xpath).getall()
        l['price'] = response.xpath(price_xpath).getall()
        l['screen'] = response.xpath(screen_xpath).getall()
        l['battery'] = response.xpath(battery_xpath).getall()
        l['processor'] = response.xpath(processor_xpath).getall()
        l['RAM'] = response.xpath(RAM_xpath).getall()
        l['ssd_memory'] = response.xpath(ssd_memory_xpath).getall()
        l['graphic_card'] = response.xpath(graphic_card_xpath).getall()
        l['laptop_type'] = response.xpath(laptop_type_xpath).getall()
        l['case'] = response.xpath(case_xpath).getall()
        l['system'] = response.xpath(system_xpath).getall()
        
        yield l
    
  