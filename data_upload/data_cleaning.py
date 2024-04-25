# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 18:08:37 2024

@author: pushy
"""

#%%
# libraries
import requests 
from bs4 import BeautifulSoup 
import re


file_path = 'data.txt'
links_path = 'links.txt'
quotes = []
mock_user = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'
}

# return soup
def get_content(URL, headers):
    if headers: 
        r = requests.get(URL, headers = mock_user)
    else:
        r = requests.get(URL)
    return BeautifulSoup(r.content, 'html5lib') 

#%%
with open(links_path, 'r') as file:
    sources = file.read()

# extract links
pattern = r'- (.+)'
sources = re.findall(pattern, sources)

#%% site number 1 and 2 (same site but different articles)

for i in range(2):
    data = []
    soup = get_content(sources[i], False)
    
    # unfiltered findall
    paras = soup.find_all('p')
    
    for para in paras:
        # exclude advert, quotes are numbered
        if para.text[0].isnumeric():
            # all quotes are in ' x. "blah blah" -author' format
            pattern = r'"([^"]*)" —'
            splits = re.findall(pattern, para.text)
            quotes.extend(splits)
            
#%% site number 3 is just <p> 

soup = get_content(sources[2], True)
paras = soup.find_all('p')
results = [x.text for x in paras]
# manually selecting as only top 3 and bottom 3 are not quotes
results = results[2:-3]

quotes.extend(results)

#%% site number 4 is just <ul>
soup = get_content(sources[3], True)
ul_tags = soup.find_all('ul', attrs ={'class':'break-above body-ul body-list-el'})
paras = []
for tag in ul_tags:
    li_tags = tag.find_all('li')
    paras.extend([x.text for x in li_tags])

quotes.extend(results)
        
#%%
with open(file_path, 'w') as file:
    for string in quotes:
        file.write(string + "\n")