from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Init:
PATH = "C:\Program Files (x86)\WebDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

domain = 'https://www.euro.com.pl'

# Variable that reduces the number of scrapped pages to 100
# True - only 100 pages, False - all pages
pages100 = True

####################################################
# Functions used in project

def scrap_links(driver,xpath_links,links_list):
    # function collects links to offers and adds them to the links' list
    # driver - chromedriver, links_list - list with links, 
    # xpath_links - xpath for finding elements
    
    # collecting all tags with links on page
    links_taken = driver.find_elements_by_xpath(xpath_links)
    for link in links_taken:
        # adding created links to the link_list
        links_list.append(link.get_attribute("href"))

def get_data(driver):
    # function collects data from webpage and return it using dictionary 
    # bs- page soup
    
    # get brand
    brand_xpath = '//a[@class="product-brand"]'
    try:
        brand = driver.find_element_by_xpath(brand_xpath).text.strip()
    except:
        brand = ""

    # get price
    price_xpath = '//div[@class="suite-main-product"]//div[@class="product-price"]/child::div'
    try:
        price = driver.find_element_by_xpath(price_xpath).text
        price = price.strip()
    except:
        price = ""

    # get screen diagonal
    screen_xpath = '//a[@title="Przekątna matrycy - laptopy"]/parent::td/following-sibling::td'
    try:
        screen = driver.find_element_by_xpath(screen_xpath).text.strip()
        # spliting the data into 2 variables
        screen2 = screen.split(', ')
        diagonal = screen2[0]
        screen = screen2[1]
    except:
        diagonal = ""
        screen = ""

    # get battery
    battery_xpath = '//a[@title="Pojemność baterii - laptopy"]/parent::td/following-sibling::td'
    try:
        battery = driver.find_element_by_xpath(battery_xpath).text
    except:
        battery = ""

    # get processor
    processor_xpath = '//tbody//a[@title="Rodzaj procesora"]/parent::td/following-sibling::td'
    try:
        processor = driver.find_element_by_xpath(processor_xpath).text.strip()
    except:
        processor = ""

    # get RAM
    RAM_xpath = '//tbody//a[@title="Pamięć RAM"]/parent::td/following-sibling::td'
    try:
        RAM = driver.find_element_by_xpath(RAM_xpath).text.strip()
    except:
        RAM = ""

    # get Graphic card
    Graphic_card_xpath = '//tbody//a[@title="Karta graficzna - komputery"]/parent::td/following-sibling::td'
    try:
        Graphic_card = driver.find_element_by_xpath(Graphic_card_xpath).text.strip()
    except:
        Graphic_card = ""

    # get memmory
    ssd_memmory_xpath = '//tbody//a[@title="Dysk twardy SSD (Solid State Drive)"]/parent::td/following-sibling::td'
    try:
        ssd_memmory = driver.find_element_by_xpath(ssd_memmory_xpath).text.strip()
    except:
        ssd_memmory = ""

    # get laptop type
    laptop_type_xpath = '//tbody//a[@title="Typy laptopów"]/parent::td/following-sibling::td'
    try:
        laptop_type = driver.find_element_by_xpath(laptop_type_xpath).text.strip()
    except:
        laptop_type = ""

    # get system
    system_xpath = '//td[contains(text(), "System operacyjny")]/following::td[1]'
    try:
        system = driver.find_element_by_xpath(system_xpath).text.strip()
    except:
        system = ""

    # creating dictionary with data
    laptop = {'brand':brand, 'price':price, 'screen':screen, 
            'diagonal':diagonal,'battery':battery, 
            'processor':processor,'RAM':RAM,'ssd_memmory':ssd_memmory,
            'graphic_card':Graphic_card, 'laptop_type':laptop_type,
            'system':system}

    return laptop

#######################################################
# Turning on the browser

url = 'https://www.euro.com.pl/laptopy-i-netbooki.bhtml' 
driver.get(url)

# waiting for browser and page start working (slow internet)
time.sleep(15)

#######################################################
# Scraping first page
# extra data are scraped from this page, which is way we don't include it in loop

# accepting cookies by clicking on 'accept' button
cookies_accept = driver.find_element_by_id('onetrust-accept-btn-handler')
cookies_accept.click()
time.sleep(5)

# Scrapping number of pages linking to offers
# last_page variable will be used to create all available links
last_page = driver.find_element(By.XPATH,'//div[@class="paging "]//span[@class="paging-dots"]/following-sibling::a')
last_page = last_page.text.strip()
time.sleep(0.3)


# collecting links to laptops from the first site using scrap_links function
links_list = []

#xpath for tag with links
xpath_links = '//div[@id="products"]//div[@class="product-row"]//a[@class="js-save-keyword"]'

scrap_links(driver,xpath_links,links_list)
time.sleep(2)

###########################################################
# Scraping links

# creating list with links to pages using last_page variable. 
# This variable represents the number of the last existing page
page_with_offers_links = []
for i in range(2,int(last_page)+1):
    link = domain + '/laptopy-i-netbooki,strona-' + str(i) + '.bhtml'
    page_with_offers_links.append(link)

# a loop collecting links to offers
for url in page_with_offers_links:

    # loading the page
    driver.get(url)
    time.sleep(5)
    
    # taking offers links using scrap_links function
    scrap_links(driver,xpath_links,links_list)
    time.sleep(0.3)

    # reducing number of pages visited in this step, when variable pages100 is used
    if pages100 == True:
        if len(links_list) >= 100:
            break


# trash collecting from fist step
del page_with_offers_links, cookies_accept, last_page, xpath_links

###########################################################
# Scraping data from offers


# reducing number of links scraped in first step

# the previous if statement only truncates a page count.
# at the moment of breaking the loop, the number of pages is approximately 112. 
# therefore, the remaining 12 links must be removed using the code below

if pages100 == True:
    if len(links_list) >= 100:
        links_list = links_list[0:100]

# preparing data frame for data
data = pd.DataFrame({'brand':[], 'price':[], 'screen':[], 'diagonal':[],
                    'battery':[], 'processor':[], 'RAM':[], 
                    'ssd_memmory':[], 'Graphic_card':[], 'laptop_type':[],
                    'system':[]})

time.sleep(2)

###########################################################
# Scraping data from offers

# a loop collecting data from offers 
for url in links_list:

    # loading the page
    driver.get(url)
    time.sleep(5)

    # clicking on 'expand technical details' button
    expand = driver.find_element(By.XPATH, '//*[@id="expand-specification"]')
    expand.click()

    time.sleep(5)

    #scraping data with get_data function
    laptop_data = get_data(driver)

    #collecting the data
    data = data.append(laptop_data, ignore_index = True)

    time.sleep(1)

# close browser
driver.quit()

##############################################################
# Saving data to csv

data.to_csv('laptops-selenium.csv')

