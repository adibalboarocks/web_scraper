import pymongo
from datetime import datetime, date
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Scraped_data"]

def store(username,email, scraped_dict):
    print(username)
    print(email)
    current_time = datetime.now()
    current_date= datetime.now().date()
    time_string = current_time.strftime('%H:%M:%S')+"___"+current_date.strftime(r'%Y-%m-%d')
    scraped_dict['_id']=time_string
    mycollection= mydb[username]
    x = mycollection.insert_one(scraped_dict)
    mylog=mydb["user_log"]
    y={'username':username,'email':email,'relational_id':time_string}
    z=mylog.insert_one(y)
    print(z)

