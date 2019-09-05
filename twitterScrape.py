'''
© HALSmartia 2019

Algorithm scrapes tweets from the past week
to determine social sentiment factor for 
a particular search. 

@author: Adrian Melendez Relli

Dependencies: PANDAS, TWEEPY, INDICOIO, OS

@param: Brand Search Query, Number Tweets, Output Path
-Twitter imposes a rate limit, resets every 15 minutes

@output: CSV file to specified path
'''

#impport statements
import pandas as pd
import tweepy
import indicoio
import os



'''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''

#class constants (apply filters as necessary)
brand = 'S10 -filter:retweets'

#Number of tweets to fetch (recommended limit to prevent timeout - 1000)
numTweets = 500

#Local output path
outputPath = 'PATH'

#Language to search (use standard 2-character ISO Code)
language = 'es'

#API Keys
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'
indicoio.config.api_key = 'INDICOIO API KEY'

'''~~~ FILL INFORMATION ABOVE THIS LINE ~~~''' 
 
 

#Authentication
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)

#Create columns for output csv
tweets_dict = {"Text":[],"Retweets":[], "Favorites":[], "Date": [], "Sentiment": [], "User Followers": [], "Username": [], "Location": [], "Verified": [], "Profile Picture": []}

count = 1
for tweet in tweepy.Cursor(api.search, q=brand, lang = language).items(numTweets):
    print('Tweet: ' + str(count))
    tweets_dict["Text"].append(tweet.text)
    tweets_dict["Retweets"].append(tweet.retweet_count)
    tweets_dict["Favorites"].append(tweet.favorite_count)
    tweets_dict["Date"].append(tweet.created_at)
    tweets_dict["Sentiment"].append(indicoio.sentiment(tweet.text))
    tweets_dict["User Followers"].append(tweet.user.followers_count)
    tweets_dict["Username"].append(tweet.user.screen_name)
    tweets_dict["Location"].append(tweet.user.location)
    tweets_dict["Verified"].append(tweet.user.verified)
    tweets_dict["Profile Picture"].append(tweet.user.profile_image_url_https)
    count+=1

#Make Dataframe
tweets_data = pd.DataFrame(tweets_dict)

#Print dataframe
print(tweets_data)

#Output csv file
filename = brand + 'Twitter' + '.csv'
tweets_data.to_csv(os.path.join(outputPath, filename), index = False)