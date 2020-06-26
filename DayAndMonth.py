#!/usr/bin/env python
# coding: utf-8

# In[4]:


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


# In[5]:


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


# In[6]:


def prepareResultForMonth(df):
    result={}
    for key,value in df.iterrows():
        if value['date'] in result.keys():
            result[value['date']][value['value']]+=1
            result[value['date']]['total']+=1
        else:
            result[value['date']]={'negative':0,'neutral':0,'positive':0,'total':0}
            result[value['date']][value['value']]+=1
            result[value['date']]['total']+=1
    percentage={}
    for date in result.keys():
        percentage[date]={'negative':0,'neutral':0,'positive':0}
        percentage[date]['negative']= result[date]['negative']/result[date]['total']
        percentage[date]['neutral']= result[date]['neutral']/result[date]['total']
        percentage[date]['positive']= result[date]['positive']/result[date]['total']
    return [result,percentage]


# In[7]:


def prepareResultForDay(df,date):
    result={}
    df_date=df[df['date']==date]
    for key,value in df_date.iterrows():
        if value['time'][:2] not in result.keys():
            result[value['time'][:2]]={'positive':0,'negative':0,'neutral':0,'total':0}
        result[value['time'][:2]][value['value']]+=1
        result[value['time'][:2]]['total']+=1
    return result


# In[16]:


def driverFunction():
    indian_tweets=pd.read_csv('D:\\Kartik_PersonalData\\IBM_Hackathon\\' + 'FinalIndianTweets' + '.csv')
    result_month, percentage_month = prepareResultForMonth(indian_tweets)
    dates = indian_tweets['date'].unique()
    result_for_day={}
    for date in dates:
        result = prepareResultForDay(indian_tweets,date)
        result_for_day[date]=result
    
#     print(result_for_day)
#     print(result_month)
    
    a_file = open("monthData.pkl", "wb")
    pickle.dump(percentage_month, a_file)
    a_file.close()
    
    a_file = open("dayData.pkl", "wb")
    pickle.dump(result_for_day, a_file)
    a_file.close()


# In[17]:


driverFunction()


# In[ ]:




