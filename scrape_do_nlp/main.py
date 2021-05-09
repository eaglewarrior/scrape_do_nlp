__version__ = "1.0.0"
### Importing all the packages
import requests
import urllib.request
import time
import spacy
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
import re
import unicodedata
from nltk.corpus import stopwords
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt') # one time execution
import re
from nltk.tokenize import sent_tokenize
from gensim.summarization import summarize
import re

#### Cleaning text 
### reference (https://github.com/kaparker/gameofthrones-wordclouds/blob/master/gotwordcloud.py)

def removetitle(text):
    return re.sub(r'.*:', '', text)

def removebrackets(text):
    return re.sub('[\(\[].*?[\)\]]', ' ', text)

def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_special_chars(text, remove_digits=False):
    pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
    return re.sub(pattern, '', text)

def remove_stopwords(text):
    stopword_list = stopwords.words('english')
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return ' '.join([token for token in tokens if token not in stopword_list])

def lemmatize(text):
    text = nlp(text)
    return ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])

### Wrapper function to call all the clean functions at once
def clean_text(txt):
    text_title=removetitle(txt)
    text_brackets=removebrackets(text_title)
    text_clean=remove_accented_chars(text_brackets)
    text_clean=text_clean.lower()
    text_clean=remove_special_chars(text_clean)
    text_clean=remove_stopwords(text_clean)
    return text_clean
def get_data_from_google(numResults,topic):
    """
    It takes two argument
    numResults: Number of results you want to extract
    topic: The topic for which you want to extract data
    """
    url ="https://www.google.com/search?q="+topic+"&tbm=nws&hl=en&num="+str(numResults)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all("div", attrs = {"class": "ZINbbc"})
    descriptions = []
    for result in results:
        try:
            description = result.find("div", attrs={"class":"s3v9rd"}).get_text()
            if description != "": 
                descriptions.append(description)
        except:
            continue
    text = "".join(descriptions)
    google_text_data=[x if len(x)>20 else np.nan for x in text.split(".")]
    google_text_data=[x for x in google_text_data if x == x]
    return google_text_data

def sentiment(data_list):
    """
    Takes list of sentences as input and gives sentiment score as output
    """
    for x in data_list:
        print(x)
        analysis = TextBlob(x)
        print(analysis.sentiment)
def extract_tweets(consumer_key,consumer_secret,access_token,access_token_secret,search_key):
    """
    Takes the keys and search key e.g. Omdena etc for which you want to extract data as input and gives list of tweets as output 
    """
    # Step 1 - Authenticate
    consumer_key= str(consumer_key)
    consumer_secret= str(consumer_secret)

    access_token=str(access_token)
    access_token_secret=str(access_token_secret)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #Step 3 - Retrieve Tweets
    public_tweets = api.search(search_key)
    tweets_list=[]
    for tweet in public_tweets:
        tweets_list.append(tweet.text)
    return tweets_list
def normalize_document(doc):
    stop_words = nltk.corpus.stopwords.words('english')
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
    doc = doc.lower()
    doc = doc.strip()
    # tokenize document
    tokens = nltk.word_tokenize(doc)
    # filter stopwords out of document
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc

def get_summarization(text):
    """
    It takes document or whole corpus in str format and gives summary as output
    """
    DOCUMENT = re.sub(r'\n|\r', ' ', text)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()
    print("Summary 1")
    print(summarize(DOCUMENT, word_count=75, split=False))
    print("Summary 2")
    print(summarize(DOCUMENT, ratio=0.2, split=False))
def get_summary(topic,consumer_key,consumer_secret,access_token,access_token_secret,numResults,sentiment_flag=False):
    
    google_list=get_data_from_google(numResults,topic)
    tweet_list=extract_tweets(consumer_key,consumer_secret,access_token,access_token_secret,topic)
    final_list=google_list+tweet_list
    if sentiment_flag:
        sentiment(final_list)
    document='.'.join(final_list)
    get_summarization(document)
    