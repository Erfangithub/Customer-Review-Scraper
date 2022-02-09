import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time


def is_date(date_string, format="%m/%d/%Y"):
    try:
        datetime.strptime(date_string, format)
        return True

    except ValueError:
        return False


# scrapeinfo arguments guide:

#- daterange = ['yyyy/mm/dd', 'yyyy/mm/dd']
#- pagerange = [initialpage , finalpage]
#- scrapemode = 'page' # scrapes reviews based on page range, page = 0,1,2,...
#               'date' # scrapes reviews based on date range
#               'allpages' # scrapes reviews from all pages related to the business on Yelp website 
#- business_phrase = the phrase of the restaurant business in its yelp website url
# e.g.:
# scrapeinfo = {'daterange':['2015/01/15', '2016/01/15'], 'pagerange' : [0 , 5],
# 'business_phrase':'richmond-station-toronto', 'scrapemode' : 'date'}

def scrape(scrapeinfo:dict, starttime, scrapetime):

    daterange = scrapeinfo['daterange']
    pagerange = scrapeinfo['pagerange']
    scrapemode = scrapeinfo['scrapemode']
    business_phrase = scrapeinfo['business_phrase']    

    sdate = datetime.strptime(daterange[0], '%Y/%m/%d')
    edate = datetime.strptime(daterange[1] , '%Y/%m/%d')

    totreviews = []
    totdates = []

# get the text content of the first page of reviews sorted by date descending
    url = f"https://www.yelp.com/biz/{business_phrase}?sort_by=date_desc"
    req = requests.get(url)
    bsObj = BeautifulSoup(req.text, "html.parser")

# Finding total number of reviews of the business at Yelp site
    l = bsObj.find('title').getText().split(' ')
    for i, item in enumerate(l):
        if item.lower() == 'reviews' and l[i-1].isdigit():
            numreviews = int(l[i-1])

# Finding total number of pages for the reviews (each page contains 10 reviews)
    numpages = int(numreviews/10)

    if scrapemode == 'page':
        page = pagerange[0]
        endpage = pagerange[1]

    if scrapemode == 'allpages' or scrapemode == 'date':
        page = 0
        endpage = numpages

    condition = True

    while page <= endpage and condition:

        # get the html text of the page number {page}
        start = page*10
        url = f"https://www.yelp.com/biz/{business_phrase}?start={str(start)}&sort_by=date_desc"
        req = requests.get(url)
        bsObj = BeautifulSoup(req.text, "html.parser")

        # get the reviews of page {page}
        reviews = []
        spanreview = bsObj.findAll('span', class_ = "raw__09f24__T4Ezm") #, lang = "en")
        for item in spanreview:
            if 'lang' in item.attrs.keys():
                reviews.append(item.getText())

        # get the date of reviews of page {page}
        dates = []        
        spandate = bsObj.findAll('span', class_ = "css-1e4fdj9")
        for item in spandate:
            strg = item.getText()
            if is_date(strg):
                dates.append(strg)


        # add the reviews and dates scraped to totreviews and totdates
        if scrapemode == 'page' or scrapemode == 'allpages':
            totreviews+=reviews
            totdates+=dates
        
        # add the reviews and dates scraped to totreviews and totdates for
        # dates that are within the desired date range.
        if scrapemode == 'date':
            revs = []
            dts = []

            for review, date in zip(reviews, dates):
                datef = datetime.strptime(date, '%m/%d/%Y')
                if (datef >= sdate) and (datef <= edate):
                    revs.append(review)
                    dts.append(date)
            
            if len(dts) == 0:
                if len(dates) > 0:
                  datef = datetime.strptime(dates[0], '%m/%d/%Y')
                  if datef < sdate:
                      condition = False

            totreviews+= revs
            totdates+=dts

        end = time.time()
        interval = end - starttime
        if interval > scrapetime:
            return totreviews, totdates

        # wait for a random time between 8 and 14 seconds before scraping next page to avoid getting blocked
        time.sleep(np.random.randint(8,14))

        # increase page by 1
        page += 1

    return totreviews, totdates
