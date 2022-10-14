import pandas as pd
import numpy as np
import re
from requests import get
from bs4 import BeautifulSoup as bs

#####################################

#make function
def get_blog_urls(base_url, header = {'User-Agent': 'hamsandwich'}):
    '''
    this function takes in base url and gets content and returns links of blog posts
    '''
    soup = bs(get(base_url, headers = header).content)

    #return links
    return [link["href"] for link in soup.select("a.more-link")]


def get_blog_content(base_url):
    '''
    this function takes in base url, creates links to each blogs and returns title and heading
    '''
    #create link
    blog_links = get_blog_urls(base_url)
    all_blogs = []
    for blog in blog_links:
        blog_soup = bs(
            get(blog, headers= {'User-Agent': 'hamsandwich'}).content)
        blog_content = {'title': blog_soup.select_one('h1.entry-title').text,
        'content': blog_soup.select_one('div.entry-content').text.strip()}
        all_blogs.append(blog_content)
    return pd.DataFrame(all_blogs)


################################################

def get_cats(base_url):
    '''
    this function will give back category of articles from base url
    '''
    soup = bs(get(base_url).content)
    
    return [cat.text.lower() for cat in soup.find_all("li")[1:]]



def get_all_shorts(base_url):
    '''
    This function takes in base url, creats url for each categories, scraps out titles and bodies and returns 
    a list of dictionaries with title text and body text in dictionaries
    '''
    
    #get category from earrlier function
    cats = get_cats(base_url)
    all_articles = []
    for cat in cats:
        #create url for each category
        cat_url = base_url + "/" + cat
        #print(get(cat_url))
        #grab content
        cat_soup = bs(get(cat_url).content)
        #grab title
        cat_titles = [title.text for title in cat_soup.find_all('span', itemprop='headline')]
        #grab body
        cat_bodies = [body.text for body in cat_soup.find_all('div', itemprop='articleBody')]
        #create a dictionary
        cat_articles = [{"title":title, "category": cat, "body":body} for \
                       title, body in zip(cat_titles, cat_bodies)]
        #print('cat articles length: ',len(cat_articles))
        
        # add on dictionary as function loops
        all_articles.extend(cat_articles)
        #print('length of all_articles: ', len(all_articles))
        
    return pd.DataFrame(all_articles)