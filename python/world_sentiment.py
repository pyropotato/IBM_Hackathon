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

pd.set_option('display.max_colwidth', 400)

def addDateTime(df):
    date=[]
    #time=[]
    for _,value in df.iterrows():
        date_time_obj = dt.datetime.strptime((value['created_at'][:10] + ' ' +  value['created_at'][11:19]), '%Y-%m-%d %H:%M:%S')
        date.append(date_time_obj.date())
        #time.append(date_time_obj.time())
    df['date']=date
    #df['time']=time
    return df

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
    #print(df.head(5))
    return df

def sentimentAnalysis(df):
    #4 new columns added to dataframe-> neg,neu,pos,compound
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = df['text_ed'].apply(lambda x: sid.polarity_scores(x))
    sent_scores_df = pd.DataFrame(list(sentiment_scores))
    df_new = pd.concat([df.reset_index(drop=True), sent_scores_df.reset_index(drop=True)], axis=1)
    df_new['value']=df_new['compound'].apply(lambda x : 'neutral' if (x>-0.01 and x<0.01) else ('positive' if x>=0.01 else 'negative'))
    return df_new

def count_country_senti(df):
    country_dict = {}
    country_dict = { key : {'Positive':0,'Neutral':0,'Negative':0} for key in countries }
    #print(df)
    for _,value in df.iterrows():
        country = value['country_code']
        val = value['value']  #sentiment
        if val == 'negative':
            country_dict[country]['Negative'] += 1
        elif val == 'neutral':
            country_dict[country]['Neutral'] += 1
        elif val == 'positive':
            country_dict[country]['Positive'] += 1
    return country_dict
    

def driverFunction(dataset_dir):
    global country_senti_dict
    for file in sorted(os.listdir(dataset_dir)):
        tweets = pd.read_csv(r"dataset/%s"%(file))
        date_time_obj = dt.datetime.strptime(file[:10],'%Y-%m-%d')
        date = date_time_obj.date()
        tweets = tweets.loc[(tweets['lang']=='en') & tweets['country_code'].notnull()][['country_code','text', 'created_at']]
        tweets = addDateTime(tweets)
        tweets = processTweetText(tweets)
        tweets = sentimentAnalysis(tweets)
        tweet_count = count_country_senti(tweets)
        country_senti_dict[date] = tweet_count
        print(file)

dataset_dir = "dataset/"
st = time.time()
country_senti_dict = {}
countries_pkl = open('country_list.pkl', 'rb')      
countries = pickle.load(countries_pkl) 
driverFunction(dataset_dir)
with open('country_senti_dict.pkl', 'wb') as handle:
        pickle.dump(country_senti_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
en = time.time()
print(en - st)

