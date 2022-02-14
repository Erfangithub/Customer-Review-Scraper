from yelpscraper import scrape
import pandas as pd
import time

start = time.time()

                    ### SET SCRAPING PARAMETERS BELOW ###

scrapetime = 840  # maximum scrape time in seconds

business_phrase = 'panera-bread-toronto-3' # the phrase of the restaurant business in its yelp website url
# e.g. One of the branches of Panera Bread restaurants has a Yelp url of:
# https://www.yelp.ca/biz/panera-bread-toronto-3

# specify whether to scrape based on page range or date range or to scrape all pages:
scrapemode = 'date'
# scrapemode = 'page' or scrapemode = 'date' or scrapemode = 'allpages'

# date range to scrape
daterange = ['2018/01/15', '2022/01/15']  # ['yyyy/mm/dd', 'yyyy/mm/dd']

# page range to scrape
pagerange = [0, 1] # [initialpage , finalpage]

# local or AWS-Lambda implementation of Yelp scraper
impln = 'local'
# impln = 'local' or impln = 'AWS-Lambda'

# SCRAPING PARAMETERS RELATED TO AWS-LAMBDA IMPLEMENTATION:

# table name in dynamodb to store the scraping results
tablename = 'yelp_panera-bread-toronto-3'

# set scrape_latest_reviews to True to scrape latest reviews not stored in table tablename
scrape_latest_reviews = False

                    ### SET SCRAPING PARAMETERS ABOVE ###

# get_unscraped_date_range returns a date range [date1str, date2str] where:
# date1str = latest date stored in table tablename + 1 day
# date2str = present date - 1 day
if impln == 'AWS-Lambda' and scrape_latest_reviews:
    from dynamodb_related import get_unscraped_date_range
    daterange = get_unscraped_date_range(tablename = tablename) # use this daterange if interested in getting
    scrapemode = 'date'                                         # the latest date range of reviews not stored
                                                                # in tablename

scrapeinfo = {'daterange':daterange, 'pagerange':pagerange,
'business_phrase':business_phrase, 'scrapemode':scrapemode}


def lambda_handler(event, context):
    
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
    print("Total code runtime in seconds:",end - start)
