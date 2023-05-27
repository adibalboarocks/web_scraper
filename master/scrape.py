import datetime
from master import telecom_scrape
from master import telecom_ramblings
from master import telecom_tech_news
from master import telecom_talk



def router(date1,date2,selected_choices,selected_options):
    header_para={'header':[],'website':[],'para':[]}
    try:
        a=date1[5:16]
        if a[8:11]=='May':
            date_1 = datetime.datetime.strptime(a, r"%d %B %Y")
        else:date_1 = datetime.datetime.strptime(a, r"%d %b %Y")
        date_a = date_1.strftime(r"%d-%b-%Y")
        date_a = datetime.datetime.strptime(date_a, r"%d-%b-%Y")

        b=date2[5:16]
        if b[8:11]=='May':
            date_2 = datetime.datetime.strptime(b, r"%d %B %Y")
        else:date_2 = datetime.datetime.strptime(b, r"%d %b %Y")
        date_b = date_2.strftime(r"%d-%b-%Y")
        date_b = datetime.datetime.strptime(date_b, r"%d-%b-%Y")
    except Exception: pass
    
    try:
            if "option1" in selected_choices:
                a=telecom_scrape.route1(date_a,date_b,"https://telecoms.com/news/")
                header_para["header"]+=a['header']
                header_para['website']+=a['website']
                header_para["para"]+=a['para']
                
            if "option2" in selected_choices:
                b=telecom_ramblings.ramblings_scraper(date_a,date_b, "https://www.telecomramblings.com/",'False')
                header_para["header"]+=b['header']
                header_para['website']+=b['website']
                header_para["para"]+=b['para']
    except Exception:pass
       
    
    try:
        if "option1" in selected_options:
            c=telecom_tech_news.tech_scraper()
            header_para["header"]+=c['header']
            header_para['website']+=c['website']
            header_para["para"]+=c['para']
        if "option2" in selected_options:       
                d=telecom_talk.talk_scraper()
                header_para["header"]+=d['header']
                header_para['website']+=d['website']
                header_para["para"]+=d['para']
    except Exception:pass
    return header_para


    
    
