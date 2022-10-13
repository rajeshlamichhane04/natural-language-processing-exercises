import pandas as pd
import numpy as np
import re
from requests import get
from bs4 import BeautifulSoup as bs

#make function
def get_blog_urls(base_url, header = {'User-Agent': 'hamsandwich'}):
    soup = bs(get(url, headers = header).content)
    return [link["href"] for link in soup.select("a.more-link")]


def get_blog_content(base_url):
    blog_links = get_blog_urls(base_url)
    all_blogs = []
    for blog in blog_links:
        blog_soup = bs(
            get(blog,
                headers=header).content)
        blog_content = {'title': blog_soup.select_one(
            'h1.entry-title').text,
        'content': blog_soup.select_one(
            'div.entry-content').text.strip()}
        all_blogs.append(blog_content)
    return all_blogs