__author__ = 'Spiderman'

import requests
from requests_oauthlib import OAuth1
from random import randint
from time import sleep
from sys import argv, exc_clear, exc_info

#If you want my Twitter OAuth key, shoot me an email at suckmyspiderdick@gmail.com
authkey = OAuth1('')
previousTrend = 'goddamnit python';
#Used to grab tweets and trends from a specific region. Current is USA, 0 is worldwide.
woeid = 23424855

def main():
    while True:
         getTweet(pickTrend(getTrends()))
	 sleep(75)
	 #Sleep is to ensure you stay within the Twitter rate limits, plus a little cushion

#This will get your Twitter account suspended.
def followUser(user):
    requests.post('https://api.twitter.com/1.1/friendships/create.json?user_id=' + user["id_str"] + '&follow=true', auth=authkey)


def getTweet(trends):
    tweets = requests.get('https://api.twitter.com/1.1/search/tweets.json?q='+trends["query"], auth=authkey).json()
    
    #Tweet randomly chosen
    chosenTweet = tweets["statuses"][randint(0, len(tweets["statuses"])-1)]
    
    #This was an attempt to avoid retweeting bots that tweet current trends. IIRC it didn't work very well.
    while "trend" in chosenTweet["user"]["name"].encode('ascii', 'ignore').lower():
        chosenTweet = tweets["statuses"][randint(0, len(tweets["statuses"])-1)]
        
    requests.post('https://api.twitter.com/1.1/statuses/retweet/' + chosenTweet["id_str"] + ".json", auth=authkey)
    return chosenTweet["user"]


def getTrends():
    trends = requests.get('https://api.twitter.com/1.1/trends/place.json?id=' + str(woeid), auth=authkey).json()[0]
    return trends


def pickTrend(trends):
    global previousTrend
    
    #Avoid retweeting the same trend twice in a row
    trendNum = randint(0, len(trends["trends"])-1)
    chosenTrend = trends["trends"][trendNum]
    
    while chosenTrend == previousTrend:
            trendNum = randint(0, len(trends["trends"])-1)
            chosenTrend = trends["trends"][trendNum]
            
    previousTrend = chosenTrend
    return chosenTrend


main()
