#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


def addDateTime(df):
    date=[]
    time=[]
    for key,value in df.iterrows():
        date.append(value['created_at'][:10])
        time.append(value['created_at'][11:19])
    df['date']=date
    df['time']=time
    return df


# In[3]:


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
#   df['text'] = df['text'].apply(lambda x: x.translate(str.maketrans("","",string.punctuation)))
    #should we remove short words? length less than 3 characters
    #removing stop words
#     print(df.iloc[0]['text'])
    df['text_ed'] = df['text_ed'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
#     print(df.iloc[0]['text'])
    #removing stemming
    stemmer=PorterStemmer()
    df['text_ed'] = df['text_ed'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split() if word != ' ']))
#     print(df.iloc[0]['text'])
    return df


# In[4]:


def sentimentAnalysis(df):
    #4 new columns added to dataframe-> neg,neu,pos,compound
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = df['text_ed'].apply(lambda x: sid.polarity_scores(x))
    sent_scores_df = pd.DataFrame(list(sentiment_scores))
    df_new = pd.concat([df.reset_index(drop=True), sent_scores_df.reset_index(drop=True)], axis=1)
    df_new['value']=df_new['compound'].apply(lambda x : 'neutral' if (x>-0.01 and x<0.01) else ('positive' if x>=0.01 else 'negative'))
    return df_new


# In[5]:


keys = ['china', 'chinese', 'chinesevirus', 'chinavirus', 'wuhan', 'ChineseVirus19', '#ChineseVirus19','#china', '#chinese', '#chinesevirus', '#chinavirus', '#wuhan']
key = 'chin'


# In[6]:


tweets_found = pd.DataFrame(columns = ['user_id', 'created_at', 'screen_name', 'text', 'date', 'time', 'text_ed', 'neg', 'neu', 'pos', 'compound', 'value'])


# In[7]:


def driverFunction():
    df=pd.read_csv(r"FinalIndianTweets.csv")
    df = df[['user_id', 'created_at', 'screen_name', 'text']]
    df = addDateTime(df)
    df = processTweetText(df)
    senti_df = sentimentAnalysis(df)
    return senti_df


# In[16]:


pd.set_option('display.width', None)
senti_df = driverFunction()


# In[10]:


for i in senti_df.index:
    #tweet = senti_df['text'][i].split()
    tweet = senti_df['text'][i]
    #for word in keys:
    if key in tweet:
        tweets_found = tweets_found.append(senti_df.loc[[i]])
        continue


# In[21]:


pd.set_option('display.max_colwidth', -1)


# In[19]:


tweets_found = tweets_found[['text']]


# In[22]:


tweets_found


# In[ ]:




