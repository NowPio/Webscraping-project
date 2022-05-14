from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import time

domain = 'https://www.euro.com.pl'

# Variable that reduces the number of scraped pages to 100
# True - only 100 pages, False - all pages
pages100 = True

####################################################
# Functions used in project


def scrap_links(bs,link_list):
    # function collects links to offers and adds them to the links' list
    # bs - page soup, link_list - list with links
    
    # Collecting all tags with links on page
    start_page = bs.find_all('div',{'class':'product-buttons'})
    for i in start_page:
        # adding created links to the link_list
        link_list.append(domain+i.a['href'])

def get_data(bs):
    # function collects data from webpage and return it using dictionary 
    # bs- page soup

    #get brand
    try:
        brand = bs.find('a',{'class':'product-brand'}).text.strip()
    except:
        brand = ""

    # get price
    try:
        price = bs.find('div',{'class':'suite-main-product'}).find('div',{'class':'product-price'})['data-price']
    except:
        price = ""

    # table with specifications
    table = bs.find('table',{'class':'description-tech-details js-tech-details'}) 

    # get screen diagonal
    try:
        screen = table.find('a',{'title':'Przekątna matrycy - laptopy'}).parent.find_next_sibling().text.strip()
        # spliting the data into 2 variables
        screen2 = screen.split(', ')
        diagonal = screen2[0]
        screen = screen2[1]
    except:
        diagonal = ""
        screen = ""

    # get battery
    try:
        battery = table.find('a',{'title':'Pojemność baterii - laptopy'}).parent.find_next_sibling().text.strip()
    except:
        battery = ""                     

    # get processor
    try:
        processor = table.find('a',{'title':'Rodzaj procesora'}).parent.find_next_sibling().text.strip()
    except:
        processor = "" 

    # get RAM
    try:
        RAM = table.find('a',{'title':'Pamięć RAM'}).parent.find_next_sibling().text.strip()
    except:
        RAM = ""  

    # get graphic card
    try:
        Graphic_card = table.find('a',{'title':'Karta graficzna - komputery'}).parent.find_next_sibling().text.strip()
    except:
        Graphic_card = ""  

    # get memmory
    try:
        ssd_memmory = table.find('a',{'title':'Dysk twardy SSD (Solid State Drive)'}).parent.find_next_sibling().text.strip()
    except:
        ssd_memmory = ""

    # get type
    try:
        laptop_type = table.find('a',{'title':'Typy laptopów'}).parent.find_next_sibling().text.strip()
    except:
        laptop_type = ""     

    # get system
    try:
        system = table.find('td', text=re.compile('\s*System operacyjny.*')).find_next_sibling().text.strip()
    except:
        system = ""
    
    # creating dictionary with data
    laptop = {'brand':brand, 'price':price, 'screen':screen, 
            'diagonal':diagonal,'battery':battery, 
            'processor':processor,'RAM':RAM,'ssd_memmory':ssd_memmory,
            'Graphic_card':Graphic_card, 'laptop_type':laptop_type,
            'system':system}

    return laptop

#######################################################
# Scraping first page
# extra data are scraped from this page, which is way we don't include it in loop

url = 'https://www.euro.com.pl/laptopy-i-netbooki.bhtml' 
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

# Scrapping number of pages linking to offers
# last_page variable will be used to create all available links
last_page = bs.find('div',{'class':'paging-numbers'}).find_all('a')[-1].text
last_page = last_page.strip()

# collecting links from first site using scrap_links function
links = []
scrap_links(bs,links)

###########################################################
# Scraping links - other pages

# creating list with links to pages using last_page variable. 
#  This variable represents the number of the last existing page
page_with_offerts_links = []
for i in range(2,int(last_page)+1):
    link = domain + '/laptopy-i-netbooki,strona-' + str(i) + '.bhtml'
    page_with_offerts_links.append(link)

# a loop collecting links to offers
for url in page_with_offerts_links:

    # request
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    # taking offerts links by scrapy_links function
    scrap_links(bs,links)
    time.sleep(1)

    # reducing number of pages visited in this step, when variable pages100 is used
    if pages100 == True:
        if len(links) >= 100:
            break

#trash collecting from fist step
del bs,html,page_with_offerts_links, link, last_page

###########################################################
# Scraping data from offers

# reducing number of links scraped in first step

# the previous if statement only truncates a page count.
# at the moment of breaking the loop, the number of pages is approximately 112. 
# therefore, the remaining 12 links must be removed using the code below
if pages100 == True:
    if len(links) >= 100:
        links = links[0:100]

# preparing data frame for data
data = pd.DataFrame({'brand':[], 'price':[], 'screen':[], 'diagonal':[],
                    'battery':[], 'processor':[], 'RAM':[], 
                    'ssd_memmory':[], 'Graphic_card':[], 'laptop_type':[],
                    'system':[]})

# variable to show progress of scraping in loop below
page_number = 1

# a loop collecting data from offers 
for url in links:

    # request
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    #scraping data using get_data function
    laptop_data = get_data(bs)

    #collecting the data
    data = data.append(laptop_data, ignore_index = True)

    time.sleep(1)

    #printing progress
    print(page_number)
    page_number = page_number + 1

##############################################################
# Saving data to csv

data.to_csv('laptops-bs4.csv')


