from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
from flask import request

telecom_dict={'header':[],'website':[],'para':[]}

def page_get(val):
    user_agent = request.headers.get('User-Agent')

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--accept-cookies')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(val) 
    
    cookie_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZЙ', 'abcdefghijklmnopqrstuvwxyzй'), 'cookies')]")
    for c_el in cookie_elements:
        try:
            if "continue" in str(c_el.text).lower():
                c_el.click()
        except Exception as e:
            pass

    get_url = driver.current_url
    wait = WebDriverWait(driver, 4)
    wait.until(EC.url_to_be(val))

    if get_url == val:
     page_source = driver.page_source
    return page_source



def scraper(start_date,end_date, page_source,flag):
    soup=BeautifulSoup(page_source,'lxml')
    next=soup.find('a',class_='next page-numbers')['href']
    news=soup.findAll('div',class_="search-content left")
    a_list=[]
    date_list=[]
    for i in news:
        n=i.text.split('\n')
        sp=i.find('li',class_='post-date')
        print(sp.text)
        if sp.find('span')== None:
            if sp.text[3:6]=='May':
                date_ = datetime.strptime(sp.text, r"%d %B %Y")
            else:
                date_ = datetime.strptime(sp.text, r"%d %b %Y")
            date_obj=datetime.strftime(date_,r"%d-%m-%Y")
            dates=datetime.strptime(date_obj,r"%d-%m-%Y")
            date_list.append(dates)
        else:
            cp=sp.find('span')['title']
            date_ = datetime.strptime(cp[0:10], r"%Y-%m-%d")
            date_obj=datetime.strftime(date_,r"%d-%m-%Y")
            dates=datetime.strptime(date_obj,r"%d-%m-%Y")
            date_list.append(dates)
       
        
        if dates>=start_date and dates<=end_date:
            a_list.append(i.a['href'])
    if all(start_date>any for any in date_list):
            flag='True'
    header_para={'header':[],'website':[],'para':[]}
    for i in a_list:
        page_gets=page_get(i)
        soupy=BeautifulSoup(page_gets,'lxml')
        container=soupy.find('div',class_='columns small-12 medium-7 single-post-content_text-container')
        title=container.findAll('div',class_='columns small-12')
        header_para['header'].append(title[0].text.strip())
        header_para['website']+=["https://telecoms.com/news/"]
        header_para['para'].append(title[3].text.strip())
    if a_list==[] and flag=='False':
        scraper(start_date,end_date,page_get(next),'False')
    elif a_list==[] and flag=='True':
        pass
    elif a_list!=[] and flag=='False':
        telecom_dict['header']+=header_para['header']
        telecom_dict['website']+=header_para['website']
        telecom_dict['para']+=header_para['para']
        scraper(start_date,end_date,page_get(next),'True')
    elif a_list!=[] and flag=='True':
        telecom_dict['header']+=header_para['header']
        telecom_dict['para']+=header_para['para']
        telecom_dict['website']+=header_para['website']
        scraper(start_date,end_date,page_get(next),'True')


def route1(start_date,end_date, link):
    global telecom_dict
    telecom_dict={'header':[],'website':[],'para':[]}
    page_source=page_get(link)
    scraper(start_date,end_date, page_source,'False')
    return telecom_dict