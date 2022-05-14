# Webscrapping-project

Below you can find instructions on how to run the scrapers

# Running BeautifulSoup scraper

In order to use BeautifulSoup scraper, you should run "laptops-soup.py" in 
terminal or other python interpreter, for example VS Code.

If you want to scrape more than 100 pages, change pages100 variable to "False".

Collected data will be saved in the "laptops-bs4.csv" file.

# Running Scrapy scraper

The following order is important to run the Scrapy scraper successfully:

	1. Run "pages" spider and save results to pages.csv
	2. Run "laptops_links" spider and save results to laptops_links.csv
	3. Run "laptops" spider and save results to laptops.csv


# Running Selenium scraper

In order to use Selenium scraper, you should run "laptops-selenium.py" in 
terminal or other python interpreter, for example VS Code.

If your webdriver, web browser, or PATH to geckodriver is different than the 
provided one, please make appropriate changes before running the code.
The webdriver used in the python file was copied from the class materials.

If you want to scrape more than 100 pages, change pages100 variable to "False".

Collected data will be saved in the "laptops-selenium.csv" file.
