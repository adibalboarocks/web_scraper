import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask import request

def talk_scraper():
        header_para={'header':[],'website':[],'para':[]}
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--accept-cookies')
        options.add_argument("--headless")  # Run Chrome in headless mode
        selenium_service = Service('path_to_chromedriver')  # Replace 'path_to_chromedriver' with the actual path
        driver = webdriver.Chrome(service=selenium_service, options=options)

        # Send a GET request to the URL
        driver.get("https://telecomtalk.info/category/news/technology-news/")
        time.sleep(5)  # Wait for the page to load

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Find the articles on the page
        articles = soup.find_all('article')
        next=soup.find('a',class_="next page-numbers")['href']
        a_list=[]
    # Extract information from each article
        for article in articles:
                # Extract the article link
                area = article.find('div', class_='right_news')
                link=area.find('a')['href']
                a_list.append(link)
                driver.get(link)
                time.sleep(3)  # Wait for the page to load
        # Create a new BeautifulSoup object for the article page
                article_soup = BeautifulSoup(driver.page_source, 'html.parser')   
                # Extract the headline
                headline = article_soup.find('h1', class_='headline').text.strip()
                header_para['header']+=[headline]
                header_para['website']+=["https://telecomtalk.info/category/news/technology-news/"]
                
                # Extract the paragraphs in the article
                paragraphs = article_soup.find('div', class_="post_content").find_all('p')
                string=""
                for paragraph in paragraphs:
                        string+=paragraph.text.strip() 
                header_para['para']+=[string]
        driver.quit()
        return header_para
    # Quit the Selenium driver

