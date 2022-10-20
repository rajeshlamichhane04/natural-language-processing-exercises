import pandas as pd
import numpy as np
import unicodedata
import nltk
from nltk.corpus import stopwords
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def basic_clean(string):
    #cast to lower case
    string = string.lower()
    #remove accented and non Ascii characters
    string = unicodedata.normalize("NFKD", string)\
            .encode("ascii", "ignore")\
            .decode("utf-8")
    # remove special characters
    string = re.sub(r'[^a-z0-9\s]',"", string)
    
    return string

##########################

def tokenize(string):
    #create tokenizer
    tokenize = nltk.tokenize.ToktokTokenizer()
    #use tokenizer
    string = tokenize.tokenize(string, return_str=True)
    
    return string

 ############################


def stem(string):
    #create porter stemmer
    ps = nltk.porter.PorterStemmer()
    #apply stemmer
    #this is going to give out a list
    stems = [ps.stem(word) for word in string.split()]
    #join the list back together
    string = " ".join(stems)
    
    return string

###################################################

def lemmatize(string):
    #create lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    #use lemmatizer
    #splits back a list of words
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    #join word back together
    string = " ".join(lemmas)
    
    return string
    

###############################################


def remove_stopwords(string, extra_words = [], exclude_words = []):
    # define stopword
    stopwords_list = stopwords.words("english")
    # exclude words you do not want to remove
    stopwords_list = set(stopwords_list)-set(exclude_words)
    # include extra words manauly in stop word list
    stopwords_list = stopwords_list.union(set(extra_words))
    #split lemmaztised paragraph 
    words = string.split() 
    #give me everything that is not stopword
    filtered_words = [word for word in words if word not in stopwords_list]
    #join filtered words
    string = " ".join(filtered_words)
    
    return string

#################################################################


def prepare_news_df(df):
    #change column names
    df.columns = ["title", "category", "original"]
    df = df[["category","original"]]
    #create new column that uses basic clean and tokenoze function
    df["clean"] = df.original.apply(basic_clean).apply(tokenize)
    #create new column that uses clean column and uses stem funtion 
    df["stemmed"] = df.clean.apply(stem)
    #create new column that takes in clean and applies lemmatize function
    df["lemmatized"] = df.clean.apply(lemmatize)
    df["cleaned_up"] = df.lemmatized.apply(remove_stopwords)
    return df


###########################################################################

def prepare_blog_df(df):
    #create new column that uses basic clean and tokenoze function
    df["clean"] = df.content.apply(basic_clean).apply(tokenize)
    #create new column that uses clean column and uses stem funtion 
    df["stemmed"] = df.clean.apply(stem)
    #create new column that takes in clean and applies lemmatize function
    df["lemmatized"] = df.clean.apply(lemmatize)
    df["cleaned_up"] = df.lemmatized.apply(remove_stopwords)
    return df

########################################################################

#Define a function to automate plotting bigrams
def plot_bigrams(words):
    
    word_data = {k[0] + ' ' + k[1]: v for k, v in words.to_dict().items()}
    
    word_img = WordCloud(background_color='white', width=800, height=600).generate_from_frequencies(word_data)
    
    plt.figure(figsize=(10, 6))
    
    plt.imshow(word_img)
    
    plt.axis('off')
    
    plt.show()
    
    
##########################################################################

#Create a function to automate plotting trigram
def plot_trigrams(words):
    
    word_data = {k[0] + ' ' + k[1] + ' ' + k[2]: v for k, v in words.to_dict().items()}
    
    word_img = WordCloud(background_color='white', width=800, height=600).generate_from_frequencies(word_data)
    
    plt.figure(figsize=(10, 6))
    
    plt.imshow(word_img)
    
    plt.axis('off')
    
    plt.show()