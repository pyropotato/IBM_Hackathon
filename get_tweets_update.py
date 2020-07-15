#In[]:
import io
import random
import string
import warnings
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *


# sklearn imports
#from sklearn.model_selection import train_test_split
#from sklearn.naive_bayes import MultinomialNB
#from sklearn import metrics


# python imports
import re
import json
import os
from collections import Counter
import datetime as dt


# Visualization
#from matplotlib import pyplot as plt
#from matplotlib import ticker,dates
#import seaborn as sns
#from sklearn import feature_extraction, linear_model, model_selection, preprocessing
# from wordcloud import WordCloud
#from tqdm import tqdm_notebook


# Saving models
import pickle
import tweepy

#In[]
def processTweetText(df):
    '''
    Step 1- remove links
    Step 2- lower case
    Step 3- remove punctuation
    Step 4- remove stop words
    '''
    stop_words = set(stopwords.words('english'))
    stop_words.update(['#coronaupdate','#corona','#stayhomestaysafe','#stayhomeandstaysafe','#stayathomeandstaysafe','#stayhomesavelives','#stayhome','#coronavirus', '#coronavirusoutbreak', '#coronavirusPandemic', '#covid19', '#covid_19', '#epitwitter', '#ihavecorona', 'amp', 'coronavirus', 'covid19'])
    #removing links
    df['text_ed'] = df['text'].apply(lambda x: re.sub(r"https\S+","",str(x)))
    #removing twitter handles (@user)
    df['text_ed'] = df['text_ed'].apply(lambda x: re.sub("@[\W]*","",str(x)))
    #removing special characters, numbers, punctuations
    df['text_ed'] = df['text_ed'].apply(lambda x: re.sub("[^a-zA-Z#]"," ",str(x)))
    #lower case
    df['text_ed'] = df['text_ed'].apply(lambda x: x.lower())
    df['text_ed'] = df['text_ed'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    stemmer=PorterStemmer()
    df['text_ed'] = df['text_ed'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split() if word != ' ']))
    return df

#In[]
def sentimentAnalysis(df):
    #4 new columns added to dataframe-> neg,neu,pos,compound
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = df['text_ed'].apply(lambda x: sid.polarity_scores(x))
    sent_scores_df = pd.DataFrame(list(sentiment_scores))
    df_new = pd.concat([df.reset_index(drop=True), sent_scores_df.reset_index(drop=True)], axis=1)
    df_new['value']=df_new['compound'].apply(lambda x : 'neutral' if (x>-0.01 and x<0.01) else ('positive' if x>=0.01 else 'negative'))
    return df_new

#In[]

def driver(tweets):

    #In[]


    #In[]
    #auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    #api = tweepy.API(auth,wait_on_rate_limit=True)

    #In[]:
    start = time.time()
    #tweets = tweepy.Cursor(api.search,q="#covid" + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(10)

    #In[]:
    tweets_df = pd.DataFrame(columns=['id','text'])
    for x in tweets:
        tweets_df = tweets_df.append({'id': x.id , 'text': x.full_text}, ignore_index=True)

    #print(tweets_df)
    tweets_df = processTweetText(tweets_df)
    senti = sentimentAnalysis(tweets_df)
    # print(senti)
    senti_ls = senti['value'].tolist()
    tweet_id = senti['id'].tolist()
    tweets_text = senti['text'].tolist()
    #print(senti['text'].tolist())
    senti_dict = {}
    for x in range(len(tweet_id)):
        senti_dict[tweet_id[x]] = {'value':senti_ls[x], 'text':tweets_text[x]}
    # print('\n\n')
    print(senti_dict)
    end = time.time()
    # print(end - start)

    return senti_dict