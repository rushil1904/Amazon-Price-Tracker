import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
import re

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'}
                             

def search_product(interval_count = 1, interval_hours = 6):
    tracker_file = pd.read_csv('Documents/amazon cart.csv', sep=',')
    tracker_log = pd.DataFrame()
    track_url = tracker_file.url
    now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    interval = 0
    while interval < interval_count:
        for x, url in enumerate(track_url):
            page = requests.get(url, headers = HEADERS)
            soup = BeautifulSoup(page.content, features = "lxml")
            title = soup.find(id='productTitle').get_text().strip()
            try:
                price = float(soup.find(id='priceblock_ourprice').get_text().re.sub('[$₹,]','',price).strip())
            except:
                try:
                    price = float(soup.find('a-size-base a-color-price a-color-price').get_text().re.sub('[$₹,]','',price).strip())
                except:
                    price = ''
            try:
                    soup.select('#availability .a-color-state')[0].get_text().strip()
                    stock = 'Out of Stock'
            except:
                    try:
                        soup.select('#availability .a-color-price')[0].get_text().strip()
                        stock = 'Out of Stock'
                    except:
                        stock = 'Available' 
            log = pd.DataFrame({
                'date': [now.replace('h',':').replace('m','')],
                'title': [title],
                'url': [url],
                'price': [tracker_file.price[x]],
                'current price': [price],
                'stock': [stock]
            }) 
            try:
                if price < tracker_file.price[x]:
                    subject = "Amazon Price Dropped!"
                    mailtext='The price of your product has dropped!! Buy it now:'+URL
    
                    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
                    server.ehlo()
                    server.starttls()
                    server.login('#','##')      #Enter your mail id and password
                    server.sendmail('#','##', mailtext)   #Enter subject and message of the mail
            except:
                pass
            tracker_log = tracker_log.append(log)
            print('Adding latest price')
            sleep(5)
        interval += 1
        sleep(interval_hours*1*1)
        print('end of interval '+ str(interval))
            

    last_run = glob('Amazon price check/*.csv')[-1]
    hist = pd.read_csv(last_run)
    final_df = hist.append(tracker_log,sort=False)
    final_df.to_csv(f'Amazon price check/SEARCH_HISTORY_{now}.csv', index=False)
    print("Scrapping Complete!")
