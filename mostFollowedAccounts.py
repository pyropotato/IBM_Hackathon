#!/usr/bin/env python
# coding: utf-8

# In[127]:


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


# In[128]:


def addDateTime(indian_tweets):
    # creating date and time objects
    date = []
    time = []
    for key,value in indian_tweets.iterrows():
        date_time_obj = dt.datetime.strptime((value['created_at'][:10] + ' ' +  value['created_at'][11:19]), '%Y-%m-%d %H:%M:%S')
        date.append(date_time_obj.date())
        time.append(date_time_obj.time())
    indian_tweets['date'] = date
    indian_tweets['time'] = time
    return indian_tweets


# In[135]:


def sliceDataset(indian_tweets,start_date,end_date):
    start_obj=dt.datetime.strptime(start_date,'%Y-%m-%d')
    end_obj=dt.datetime.strptime(end_date,'%Y-%m-%d')
    indian_tweets_slice = indian_tweets[(indian_tweets['date']>=start_obj.date()) & (indian_tweets['date']<=end_obj.date())]
    return indian_tweets_slice


# In[136]:


def findTop10(indian_tweets_slice):
    indian_tweets_slice_sort = indian_tweets_slice.sort_values('followers_count',ascending = False)
    indian_tweets_slice_sort_dr = indian_tweets_slice_sort.drop_duplicates(subset='user_id')
    ls = indian_tweets_slice_sort_dr.head(10)['screen_name']
    top10_followed_accounts=[]
    for value in ls.iteritems():
        top10_followed_accounts.append(value[1])
        
    top10_followed_accounts_df = indian_tweets_slice[indian_tweets_slice['screen_name']==top10_followed_accounts[0]]
    for i in range(1,len(top10_followed_accounts)):
        top10_followed_accounts_df = top10_followed_accounts_df.append(indian_tweets_slice[indian_tweets_slice['screen_name']==top10_followed_accounts[i]],ignore_index=True)

    return top10_followed_accounts_df


# In[137]:


# indian_tweets_slice_grouped = indian_tweets_slice.groupby('screen_name')
#indian_tweets_slice_sort.groupby('screen_name').first().sort_values('followers_count',ascending = False).head(10)
##indian_tweets_slice.sort_values('retweet_count',ascending=False).head(100)


# In[138]:


def createResults(top10_followed_accounts_df):
    result={'positive':0,'neutral':0,'negative':0,'total':0}
    percentage={'positive':0,'neutral':0,'negative':0,'total':0}
    for key,value in top10_followed_accounts_df.iterrows():
        result[value['value']]+=1
        result['total']+=1
    percentage['positive']=result['positive']/result['total']
    percentage['negative']=result['negative']/result['total']
    percentage['neutral']=result['neutral']/result['total']
    return [result,percentage]


# In[139]:


def driverFunction():
    start_dates = ['2020-03-29','2020-04-05','2020-04-12','2020-04-19','2020-04-26']
    end_dates = ['2020-04-04','2020-04-11','2020-04-18','2020-04-25','2020-04-30']
    indian_tweets=pd.read_csv('D:\\Kartik_PersonalData\\IBM_Hackathon\\' + 'FinalIndianTweets' + '.csv')
    indian_tweets=addDateTime(indian_tweets)
    main_result={}
    main_percentage={}
    for i in range(5):
        indian_tweets_slice=sliceDataset(indian_tweets,start_dates[i],end_dates[i])
        top10_df=findTop10(indian_tweets_slice)
        result,percentage = createResults(top10_df)
        main_result['Week'+str(i)]=result
        main_percentage['Week'+str(i)]=percentage
    print(main_percentage)


# In[140]:


driverFunction()


# In[ ]:




