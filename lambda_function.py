from yelpscraper import scrape
import pandas as pd
import time

# maximum scrape time in seconds:
scrapetime = 840  # Note: AWS Lambda can run for a maximum of 900 seconds. For
                    # local implementation scrapetime can be set to a desired
                    # value.

start = int(time.time())

# local implementation of Yelp scraper
impln = 'local'

# AWS-Lambda implementation of Yelp scraper
# impln = 'AWS-Lambda'


tablename = 'yelp_richmond-station-toronto'

business_phrase = 'richmond-station-toronto'
business_phrase = 'panera-bread-toronto'


# specify whether to scrape based on page range or date range or to scrape all pages:
# pageordate = 'page' or pageordate = 'date' or pageordate = 'allpages'
pageordate = 'date'


def lambda_handler(event, context):

# scrapeinfo arguments guide:

#- daterange = ['yyyy/mm/dd', 'yyyy/mm/dd']
#- pagerange = [initialpage , finalpage]
#- scrapemode = 'page' # scrapes reviews based on page range, page = 0,1,2,...
#               'date' # scrapes reviews based on date range
#               'allpages' # scrapes reviews for all pages related to the business on Yelp website 
#- business_phrase = the phrase of the restaurant business in its yelp website url
# e.g.:
# scrapeinfo = {'daterange':['2015/01/15', '2016/01/15'], 'pagerange' : [0 , 5],
# 'business_phrase':'richmond-station-toronto', 'scrapemode' : 'date'}

    # date
    if pageordate == 'date':
        
        # custom date range
        daterange = ['2015/01/15', '2022/01/15']

        # get_unscraped_date_range returns the latest date range from tabelname that
        # is not scraped
        if impln == 'AWS-Lambda':
            from dynamodb_related import get_unscraped_date_range
            daterange = get_unscraped_date_range(tablename = tablename)

        scrapeinfo = {'daterange':daterange, 'pagerange' : [0 , 5],
        'business_phrase':business_phrase, 'scrapemode' : 'date'}
        
        revs, dts = scrape(scrapeinfo, start, scrapetime)
    
    # page
    if pageordate == 'page':

        scrapeinfo = {'daterange':['2020/08/01', '2021/12/30'], 'pagerange' : [0 , 2],
        'business_phrase':business_phrase, 'scrapemode' : 'page'}

        revs, dts = scrape(scrapeinfo, start, scrapetime)

    # allpages
    if pageordate == 'allpages':

        scrapeinfo = {'daterange':['2020/08/01', '2021/12/30'], 'pagerange' : [0 , 10],
        'business_phrase':business_phrase, 'scrapemode' : 'allpages'}

        revs, dts = scrape(scrapeinfo, start, scrapetime)

    # store revs and dts in dynamodb table tablename
    if impln == 'AWS-Lambda':
        from dynamodb_related import store_in_dynamodb_table
        store_in_dynamodb_table(revs,dts,tablename = tablename)

    return revs, dts


if impln == 'local':

    revs, dts = lambda_handler({},{})

    df = pd.DataFrame()

    df['review'] = revs
    df['date_of_review'] = dts

    df.to_csv('scrapeddata.csv', index = False)

    end = time.time()
    print(end - start)