'''
© HALSmartia 2019

Algorithm scrapes Reddit posts
to determine social sentiment factor
for a particular search

@author: Adrian Melendez Relli

Dependencies: PRAW, PANDAS, INDICO, OS

@param: Brand Search Query, History Range, Output Path
@output: CSV file to specified path
'''

#import dependencies
import praw
import pandas as pd
import datetime as dt
import indicoio
import os



'''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''

#API login requirements
indicoio.config.api_key = 'INDICOIO API KEY'
reddit = praw.Reddit(client_id='CLIENT_ID', \
                 client_secret='CLIENT_SECRET_KEY', \
                 user_agent='API TOOL NAME', \
                 username='REDDIT USERNAME', \
                 password='REDDIT PASSWORD')

#search query
brand = 'Samsung Galaxy S10'

#Output Path (Local or Server)
outputPath = 'PATH'

#History to search (day, week, month, year)
since = 'month'

#Specify a subreddit (Set to 'all' for an unfiltered search)
subreddit = reddit.subreddit('all')
 
'''~~~ FILL INFORMATION ABOVE THIS LINE ~~~''' 
 

 
#Create columns for output csv
topics_dict = { "Post":[], "Score":[], "Upvote Ratio":[], "Comment Number": [], "subreddit": [], "Date": [], "Sentiment": []}
 
#Fill columns from posts
for submission in subreddit.search(brand, sort = 'new', time_filter = since):
    topics_dict["Post"].append(submission.title)
    topics_dict["Score"].append(submission.score)
    topics_dict["Upvote Ratio"].append(submission.upvote_ratio)
    topics_dict["Comment Number"].append(submission.num_comments)
    topics_dict["subreddit"].append(submission.subreddit.display_name)
    topics_dict["Date"].append(submission.created)
    topics_dict["Sentiment"].append(indicoio.sentiment(submission.title))

#Make Dataframe
topics_data = pd.DataFrame(topics_dict)
    
#Change Date    
def get_date(created):
    return dt.datetime.fromtimestamp(created)

#Reassign Timestamp
_timestamp = topics_data["Date"].apply(get_date)
topics_data = topics_data.assign(timestamp = _timestamp)

#Print dataframe
print(topics_data)

#Output csv file
filename = brand + 'redditScrape' + '.csv'
topics_data.to_csv(os.path.join(outputPath, filename), index = False)
