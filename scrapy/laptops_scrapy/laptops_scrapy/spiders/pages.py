import scrapy
import re

# scraping consecutive pages with links to laptops 

# define field for the links
class Link(scrapy.Item):
    link = scrapy.Field()

# define name, domains, urls and the programme to scrape the links
class PagesSpider(scrapy.Spider):
    name = 'pages'
    allowed_domains = ['https://www.euro.com.pl/']
    start_urls = ['https://www.euro.com.pl/laptopy-i-netbooki.bhtml']

    # fetch the last page and get its number 
    def parse(self, response):
        xpath = '//div[@class="paging "]//div[@class="paging-numbers"]//a[@class="paging-number" and position()=last()]/@href'		
        last_page = response.xpath(xpath).extract()[0]
        last_page_number = re.findall("[0-9][0-9]", last_page)[0]
        
	  # create links to other pages 
        pages_links = ['https://www.euro.com.pl/laptopy-i-netbooki.bhtml']
        for i in range(2, int(last_page_number) + 1):
            page_to_append = 'https://www.euro.com.pl/laptopy-i-netbooki,strona-' + str(i) + '.bhtml'
            pages_links.append(page_to_append)
        
        for page in pages_links:
            l = Link()
            l['link'] = page
            yield l
       
        
