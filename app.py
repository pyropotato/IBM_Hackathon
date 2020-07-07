from flask import *
import pickle
import datetime as dt
import get_tweets_update
import twitter_key
import tweepy 

monthData = pickle.load( open( "dashboardData/monthData.pkl", "rb" ) )
dayData = pickle.load( open( "dashboardData/dayData.pkl", "rb" ) )
mostActiveAccounts = pickle.load( open( "dashboardData/mostActiveAccounts.pkl", "rb" ) )
mostFollowedAccounts = pickle.load( open( "dashboardData/mostFollowedAccounts.pkl", "rb" ) )
mostViralAccounts = pickle.load( open( "dashboardData/mostViralAccounts.pkl", "rb" ) )
negativeReasons = pickle.load( open( "dashboardData/neg_reasons.pkl", "rb" ) )
china_sentiments = pickle.load( open( "dashboardData/china_sentiments.pkl", "rb" ) )
world_sentiments = pickle.load( open( "dashboardData/country_senti_dict_cumm.pkl", "rb" ) )

india_data={
	'monthData':monthData,
	'dayData': dayData,
	'mostActiveAccounts':mostActiveAccounts,
	'mostFollowedAccounts':mostFollowedAccounts,
	'mostViralAccounts':mostViralAccounts,
	'negativeReasons':negativeReasons
}

world_data={
	'china' : china_sentiments,
	'world_sentiments' : world_sentiments
}


auth = tweepy.OAuthHandler(twitter_key.consumer_key,twitter_key.consumer_secret)
auth.set_access_token(twitter_key.access_token, twitter_key.access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

app= Flask(__name__)

@app.route('/india')
def india():
	return render_template('india.html')

@app.route('/indiaData')
def indiaData():
	# print('get request')
	return india_data

@app.route('/world')
def world():
	return render_template('world.html')

@app.route('/worldData')
def worldData():
	return world_data

@app.route('/liveMeter')
def getLiveMeter():
	return render_template('liveMeter.html')

@app.route('/liveData')
def getLiveData():
	tweets = tweepy.Cursor(api.search,q="#covid" + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(10)
	dat = get_tweets_update.driver(tweets)
	print(dat)
	return {'data':dat}


@app.route('/liveTweetData')
def getLiveTweet():
	tweets = tweepy.Cursor(api.search,q="#covid" + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(1)
	dat = get_tweets_update.driver(tweets)
	print(dat)
	return {'data':dat}	

@app.route('/home')
def getHome():
	return render_template('home.html')

if __name__ == '__main__':
	app.run(threaded = True, debug=True)
