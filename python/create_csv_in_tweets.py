import pandas as pd
import re
from os import listdir
from os.path import isfile, join

parent_path = 'dataset/'    #path to dataset
output_folder = 'in_extra/'  #create this path

onlyfiles = [f for f in listdir(parent_path) if isfile(join(parent_path, f))]
onlyfiles = [file_name[:-4:] for file_name in onlyfiles]
#print(onlyfiles)

word_file = open(r"final_comm_words","r")
words = word_file.readline()
words_list = words.split(" ")
#words_list.remove(' ')
try:
    words_list.remove('\n')
except:
    pass
#print(words_list)


def extract_in_tweets(df, file_, words_list):
    df_no_code = df.loc[(df['lang'] == 'en') & (df['country_code'].isnull())][['user_id', 'created_at', 'screen_name','text', 'retweet_count', 'followers_count', 'favourites_count','verified']]
    in_tweets_found = df.loc[(df['country_code'] == 'IN') & (df['lang'] == 'en')][['user_id', 'created_at', 'screen_name','text', 'retweet_count', 'followers_count', 'favourites_count','verified']]
    print(df_no_code.head())
    
    for i in df_no_code.index:
        tweet = df_no_code['text'][i].split()
        for word in words_list:
            if word in tweet:
                #print(tweet)
                in_tweets_found = in_tweets_found.append(df_no_code.loc[[i]])
                continue
    
    in_tweets_found.to_csv(output_folder + file_ + '.csv', index = False)
    print(file_ + '.csv')

for file_ in onlyfiles:
    file_nm = parent_path + file_ + ".CSV"
    df = pd.read_csv(file_nm)
    extract_in_tweets(df, file_, words_list)
