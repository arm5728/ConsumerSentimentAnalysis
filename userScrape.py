'''
© HALSmartia 2019

Algorith constructs a large database
of twitter users to help train machine
learning models. A search term is required.

Specify NUMBER of users as well as the 
amount of tweets to fetch from that 
user's timeline.

Remember standard Twitter rate limits 
apply. Excessive queries may break
algorithm.

Scraping progress is output to the console.

@author: Adrian Melendez Relli

Dependencies: TWEEPY, PANDAS OS

@param: Search Query, Language, Number Users, Tweets per User
@output: CSV file to specified path
'''


'''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''

#API Keys
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

#Search Term
search = 'Hello'

#Language to search (use standard 2-character ISO Code)
language = 'es'

#Output Path (Local or Server)
outputPath = 'PATH'

#Number of users
numUsers = 100

#Number of tweets per user (MAX, may not always yield this amount)
tweetsPerUser = 250

'''~~~ FILL INFORMATION ABOVE THIS LINE ~~~''' 


#impport statements
import pandas as pd
import tweepy
import os
 

#Authentication
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication,  wait_on_rate_limit=True, wait_on_rate_limit_notify = True)

#Query Constructor
query = search + ' -filter:retweets -filter:replies'

#Create columns for output csv
tweets_dict = {"Profile Picture":[], "Username":[], "Name": [], "Location": [], "Query": [], "Text": [], "Date": [], "Followers": [], "Compiled Text": []}
countA = 1
for tweet in tweepy.Cursor(api.search, q= query, lang = language, count = 100).items(numUsers):
    print("User: " + str(countA)) 
    tweets_dict["Name"].append(tweet.user.name)
    tweets_dict["Username"].append(tweet.user.screen_name)
    tweets_dict["Profile Picture"].append(tweet.user.profile_image_url_https)
    tweets_dict["Text"].append(tweet.text)
    tweets_dict["Query"].append(query)
    tweets_dict["Date"].append(tweet.created_at)
    tweets_dict["Followers"].append(tweet.user.followers_count)
    tweets_dict["Location"].append(tweet.user.location)
    completeText = ' '
    countB = 1
    for status in tweepy.Cursor(api.user_timeline, screen_name=tweet.user.screen_name , tweet_mode="extended").items(tweetsPerUser):
        print("User: " + str(countA) + " ~ Tweet " + str(countB))
        
        #FILTER REDUNANT RETWEETS
        toAdd = status.full_text
        if "RT" not in toAdd:
            completeText = completeText + toAdd
        countB += 1
        
    tweets_dict["Compiled Text"].append(completeText)
    countA += 1
            
#Make Dataframe
tweets_data = pd.DataFrame(tweets_dict)
   
#Print dataframe
print(tweets_data)
   
#Output csv file
filename = search + 'TwitterUsers' + '.csv'
tweets_data.to_csv(os.path.join(outputPath, filename), index = False)

