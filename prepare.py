import pandas as pd
import numpy as np
import unicodedata
import nltk
from nltk.corpus import stopwords
import re

def basic_clean(original):
    #cast to lower case
    article = original.lower()
    #remove accented and non Ascii characters
    article = unicodedata.normalize("NFKD", article)\
            .encode("ascii", "ignore")\
            .decode("utf-8")
    # remove special characters
    article = re.sub(r'[^a-z0-9\'\s]',"", article)
    
    return article

##########################

def tokenize(article):
    #create tokenizer
    tokenize = nltk.tokenize.ToktokTokenizer()
    #use tokenizer
    article = tokenize.tokenize(article, return_str=True)
    
    return article

 ############################


def stem(article):
    #create porter stemmer
    ps = nltk.porter.PorterStemmer()
    #apply stemmer
    #this is going to give out a list
    stems = [ps.stem(word) for word in article.split()]
    #join the list back together
    article_stemmed = " ".join(stems)
    
    return article_stemmed

###################################################

def lemmatize(article):
    #create lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    #use lemmatizer
    #splits back a list of words
    lemmas = [wnl.lemmatize(word) for word in article.split()]
    #join word back together
    article_lemmatized = " ".join(lemmas)
    
    return article_lemmatized
