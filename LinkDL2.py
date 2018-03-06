#! python3
# LinkDL.py
# Attempt to download every link on a
# user-supplied web page

import requests, os, bs4, re
from selenium import webdriver

URL = 'https://news.ycombinator.com/'
os.makedirs('HNArticles', exist_ok=True)

print(os.getcwd())
print('Downloading today\'s top links!')
res = requests.get(URL)
res.raise_for_status()



# TODO: Find all links to open and download
soup = bs4.BeautifulSoup(res.text, "html.parser")
storylink = soup.select('.title a')
numDL = len(storylink)
if storylink == []:
    print('Could not find any stories to download :/')

# TODO: Extract all URLs from the headline title list
URLs = []
for i in range(0, numDL, 2):
    URLs.append(storylink[i].get('href'))
    i += 1

# TODO: Open each link in URLs and download the contents
for i in range(len(URLs)):
    try:
        articleURL = URLs[i]
        # Download the linked contents
        print('Downloading the page %s...' % articleURL)
        articleRes = requests.get(articleURL)
        articleRes.raise_for_status()
        articleFile = open(os.path.join('/Users/peterpelberg/Dropbox/Projects/automate-python/HNArticles/', articleURL[15:20]), 'wb')
        for chunk in articleRes.iter_content(100000):
            articleFile.write(chunk)
        articleFile.close()
        i += 1
    except requests.exceptions.HTTPError:
        continue
    except requests.exceptions.MissingSchema:
        print('There is something funky with the schema of this URL.')
        continue
    except FileNotFoundError:
        print('There was an issue downloading the contents of this page. Check the URL.')
        continue
