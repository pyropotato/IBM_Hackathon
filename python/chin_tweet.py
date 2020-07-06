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
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


# python imports
import re
import json
import os
from collections import Counter
import datetime as dt


# Visualization
from matplotlib import pyplot as plt
from matplotlib import ticker,dates
import seaborn as sns
from sklearn import feature_extraction, linear_model, model_selection, preprocessing
# from wordcloud import WordCloud
from tqdm import tqdm_notebook


# Saving models
import pickle

tweets_found = pd.DataFrame(columns = ['text', 'date', 'time'])

def addDateTime(tweets):
    # creating date and time objects
    date = []
    time = []
    for _,value in tweets.iterrows():
        date_time_obj = dt.datetime.strptime((value['created_at'][:10] + ' ' +  value['created_at'][11:19]), '%Y-%m-%d %H:%M:%S')
        date.append(date_time_obj.date())
        time.append(date_time_obj.time())
    tweets['date'] = date
    tweets['time'] = time
    return tweets

def sliceDataset(indian_tweets,start_date,end_date):
    start_obj=dt.datetime.strptime(start_date,'%Y-%m-%d')
    end_obj=dt.datetime.strptime(end_date,'%Y-%m-%d')
    indian_tweets_slice = indian_tweets[(indian_tweets['date']>=start_obj.date()) & (indian_tweets['date']<=end_obj.date())]
    return indian_tweets_slice

def find_china(tweets):
    global tweets_found
    for i in tweets.index:
        tweet = tweets['text'][i]
        if ' chin' in tweet:
            tweets_found = tweets_found.append(tweets.loc[[i]])
            continue

def driverFunction(dataset_dir):
    #start_dates = ['2020-03-29','2020-04-05','2020-04-12','2020-04-19','2020-04-26']
    #end_dates = ['2020-04-04','2020-04-11','2020-04-18','2020-04-25','2020-04-30']
    for file in sorted(os.listdir(dataset_dir)):
        tweets = pd.read_csv(r"dataset/%s"%(file))
        tweets = tweets.loc[(tweets['lang']=='en')][['text', 'created_at']]
        tweets = addDateTime(tweets)
        #print(tweets)
        find_china(tweets)
        print(file)

dataset_dir = "dataset/"
st = time.time()
driverFunction(dataset_dir)
tweets_found.to_csv("china_tweets.csv")
en = time.time()
print(en - st)
