import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta, date


def get_unscraped_date_range(tablename = 'yelp_panera-bread-toronto-3'):
    # This function returns a date range [date1str, date2str] where:
    # date1str = latest date stored in table tablename + 1 day
    # date2str = present date - 1 day

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)

# get latest date in the table
    dats = table.scan(AttributesToGet=['date_of_review'])

    datslist = []
    for item in dats["Items"]:
        if item != {}:
            datslist.append(datetime.strptime(item["date_of_review"], '%m/%d/%Y'))
    if len(datslist) > 0:
        maxdate = max(datslist)
    else:
        maxdate = datetime.strptime('01/01/1900', '%m/%d/%Y')

# date1
    date1 = maxdate + timedelta(days=1)

# store the date of 1 day before present date in date2
    todaydate = datetime.combine(date.today(), datetime.min.time())
    date2 = todaydate - timedelta(days=1)

    
# the date part of date1 and date2 in string format
    date1str = '/'.join([str(date1.year),str(date1.month),str(date1.day)])
    date2str = '/'.join([str(date2.year),str(date2.month),str(date2.day)])

    return [date1str, date2str]


def store_in_dynamodb_table(revs,dts, tablename = 'yelp_panera-bread-toronto-3'):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)
    
# get maximum id from table
    resp = table.scan(AttributesToGet=['id'])
    
    indlist = []
    
    for item in resp["Items"]:
        if item != {}:
            indlist.append(int(item["id"]))

    if len(indlist) == 0 :
        ind = 1
    else:
        ind = max(indlist) + 1


# store id, review and date_of_review in dynamodb table
    client = boto3.client('dynamodb')

    for dat, review in zip(dts, revs):
        data = client.put_item(TableName=tablename,
        Item={
            'id': {
                'S': str(ind)
            },
            'date_of_review': {
                'S': dat
            },
            'review': {
                'S': review
            }})
        
        ind+= 1
