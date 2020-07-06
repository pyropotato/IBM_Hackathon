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


# In[6]:


def addDateTime(indian_tweets):
    # creating date and time objects
    date = []
    time = []
    for _,value in indian_tweets.iterrows():
        date_time_obj = dt.datetime.strptime((value['created_at'][:10] + ' ' +  value['created_at'][11:19]), '%Y-%m-%d %H:%M:%S')
        date.append(date_time_obj.date())
        time.append(date_time_obj.time())
    indian_tweets['date'] = date
    indian_tweets['time'] = time
    return indian_tweets


# In[7]:


def sliceDataset(indian_tweets,start_date,end_date):
    start_obj=dt.datetime.strptime(start_date,'%Y-%m-%d')
    end_obj=dt.datetime.strptime(end_date,'%Y-%m-%d')
    indian_tweets_slice = indian_tweets[(indian_tweets['date']>=start_obj.date()) & (indian_tweets['date']<=end_obj.date())]
    return indian_tweets_slice


# In[34]:


def getNegativeReasons(tweets):
    neg_tweets = tweets[tweets['value'] == 'negative'][['text']]
    
    causes = {'food':['food', 'hunger', 'feeding'],
    'shelter':['shelter', 'homeless', '#shelter', '#homeless'],
    'income':['income', 'bills', '#income', '#bills'],
    'travel':['travel', 'immigrants', 'immigrant', '#travel', '#immigrants', '#immigrant', 'flights'],
    'health':['health', '#health'],
    'PPE':['PPE', 'ppe', '#PPE', '#ppe']
    }

    main_causes = list(causes.keys())
    causes_count = dict.fromkeys(main_causes, 0 )
    for _,value in neg_tweets.iterrows():
        tweet = value['text'].split()
        #print(tweet)
        for m_cause in main_causes:
            for x in causes[m_cause]:
                if x in tweet:
                    causes_count[m_cause] += 1
                    continue
    return causes_count

# In[38]:


def driverFunction():
    start_dates = ['2020-03-29','2020-04-05','2020-04-12','2020-04-19','2020-04-26']
    end_dates = ['2020-04-04','2020-04-11','2020-04-18','2020-04-25','2020-04-30']
    indian_tweets=pd.read_csv('FinalIndianTweets.csv')
    indian_tweets=addDateTime(indian_tweets)
    main_result={}
    for i in range(5):
        indian_tweets_slice=sliceDataset(indian_tweets,start_dates[i],end_dates[i])
        main_result['Week'+str(i)] = getNegativeReasons(indian_tweets_slice)
    print(main_result) 


# In[39]:
driverFunction()
