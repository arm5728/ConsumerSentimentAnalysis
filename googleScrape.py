'''
© HALSmartia 2019

Algorithm scrapes google news articles
and generates sentiment score based on 
title and heading.

SINCE this is a hacky HTML scrape, 
this may break with Google update.
Works as of 8/23/2019

@author: Adrian Melendez Relli

Dependencies: INDICOIO, PANDAS, OS, REQUESTS, BeautifulSoup, GoogleTranslator

@param: Brand Search Query, History Range, Output Path
@output: CSV file to specified path
'''

#import statements
import indicoio
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import os
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import random
import time

#Method from Simeon Babatunde, Stack Overflow
#Get Date from string
def get_past_date(str_days_ago):
    try:
        TODAY = datetime.date.today()
        splitted = str_days_ago.split()
        if len(splitted) == 1 and splitted[0].lower() == 'today':
            return str(TODAY.isoformat())
        elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
            date = TODAY - relativedelta(days=1)
            return str(date.isoformat())
        elif splitted[1].lower() in ['min', 'mins', 'minute', 'minutes']:
            date = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
            return str(date.date().isoformat())
        elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
            date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
            return str(date.date().isoformat())
        elif splitted[1].lower() in ['day', 'days', 'd']:
            date = TODAY - relativedelta(days=int(splitted[0]))
            return str(date.isoformat())
        elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
            date = TODAY - relativedelta(weeks=int(splitted[0]))
            return str(date.isoformat())
        elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
            date = TODAY - relativedelta(months=int(splitted[0]))
            return str(date.isoformat())
        elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
            date = TODAY - relativedelta(years=int(splitted[0]))
            return str(date.isoformat())
        else:
            return str_days_ago
    except IndexError:
        return str('WRONG FORMAT')



'''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''
   
#API Keys
indicoio.config.api_key = 'INDICO_KEY'

#Search Query
brand = 'Huawei Mate 20'

#Pages to scrape (WARNING: EXCESS MAY CAUSE GOOGLE IP BAN)
pages = 25

#Output Path (Local or Server)
outputPath = 'PATH'


'''~~~ FILL INFORMATION ABOVE THIS LINE ~~~'''

translator = Translator()

#Create columns for output csv
results_dict = {"Title": [], "Source": [], "Date": [], "Headline": [], "Sentiment": []}

#Scrape each page
for article in range(0, (pages * 10), 10):       
    #URL to search
    url = 'https://www.google.com/search?q={0}&source=lmns&tbm=nws&start={1}'.format(brand, article)
        
    #Parse Page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') 
       
    #Get Data, Fill columns 
    results = soup.findAll('div', class_='g')
    for result in results:
        title = result.find('h3', class_='r').get_text()
        source = result.find('div', class_='slp').get_text().split(' - ')[0]
        date = get_past_date((translator.translate(result.find('div', class_='slp').get_text().split(' - ')[1])).text)
        headline = result.find('div', class_='st').get_text() 
        combinedText = title + ' ' + headline
        
        results_dict["Title"].append(title)
        results_dict["Source"].append(source)
        results_dict["Date"].append(time)
        results_dict["Headline"].append(headline)
        results_dict["Sentiment"].append(indicoio.sentiment(combinedText))

    #Prevent Google Script Detection
    print('Completed scraping Page ' + str(int((article / 10) + 1)))
    timeout = random.randrange(1, 3)
    timeout_string = str(timeout)
    print('Anti-Timeout Delay: ' + timeout_string + ' seconds')
    time.sleep(timeout)
    print('Working on Page ' + str(int((article / 10) + 2)))
    
#Make and Print dataframe
results_data = pd.DataFrame(results_dict)
print(results_data)

#Output csv file
filename = brand + 'GoogleNews' + '.csv'
results_data.to_csv(os.path.join(outputPath, filename), index = False)
