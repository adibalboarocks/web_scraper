import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ramblings_scraper(start_date,end_date, url,flag):
    rambling_dict={'header':[],'website':[],'para':[]}
    date_list=[]
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.content, 'html.parser')
    next=soup.find('a',class_='nextpostslink')['href']
    # Find the articles on the page
    articles = soup.find_all('div', class_='entrybox')

    a_list=[]
    header_para={'header':[],'website':[],'para':[]}
    # Extract information from each article
    for article in articles:
        # Extract the article link
        link = article.find('a')['href']

        date_heading=article.find('h4')
        date_string_with_suffix=date_heading.text
        date_string = date_string_with_suffix.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
        date_obj = datetime.strptime(date_string.strip(), r"%B %d, %Y")
        formatted_date = date_obj.strftime(r"%d-%m-%Y")
        date_of_article = datetime.strptime(formatted_date, r"%d-%m-%Y")
        date_list.append(date_of_article)       

        # Send a GET request to the article link
        
        if date_of_article>=start_date and date_of_article<=end_date:
            a_list.append(link)
            print(date_of_article)
            print(link)
            article_response = requests.get(link)
            
            # Create a new BeautifulSoup object for the article page
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            headline = article_soup.find('h1', class_='entry-title').text.strip()
            header_para['header'].append(headline)
            header_para['website']+=["https://www.telecomramblings.com/"]
            
            print(headline)
            # Extract the paragraphs in the article
            paragraphs = article_soup.find('div', class_='entry').find_all('p')
            string=''
            for p in paragraphs:
                string+=p.text
            header_para['para'].append(string)

            print(header_para['header'])
            
    if all(start_date>any for any in date_list):
            flag='True'

    if a_list==[] and flag=='False':
        ramblings_scraper(start_date,end_date,next,'False')
    elif a_list==[] and flag=='True':
        pass
    elif a_list!=[] and flag=='False':
        rambling_dict['header']+=header_para['header']
        rambling_dict['website']+=header_para['website']
        rambling_dict['para']+=header_para['para']
        ramblings_scraper(start_date,end_date,next,'True')
    elif a_list!=[] and flag=='True':
        rambling_dict['header']+=header_para['header']
        rambling_dict['website']+=header_para['website']
        rambling_dict['para']+=header_para['para']
        ramblings_scraper(start_date,end_date,next,'True')
            # Extract the headline
    return(rambling_dict)

