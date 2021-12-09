import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from datetime import timedelta
import urllib3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
time_limit = 7


# returns the results for searching "query" in google places at a given location
def places_by_name(query, location, page):
    # set up the request parameters
    params = {
        'api_key': '4DE3562B07194C29AD08E554B1A467B0',
        'q': query,
        'search_type': 'places',
        'hl': 'en',
        'page': page,
        'location': location,
        'google_domain': 'google.com'
    }

    # make the http GET request to Scale SERP
    http = urllib3.PoolManager()
    api_result = http.request('GET', 'https://api.scaleserp.com/search', fields=params)
    return json.loads(api_result.data.decode('utf-8'), parse_float=Decimal)


# gets all the reviews of a place by its place_id
def reviews_by_id(place_id):
    # set up the request parameters
    params = {
        'api_key': '4DE3562B07194C29AD08E554B1A467B0',
        'search_type': 'place_reviews',
        'data_id': place_id,
        'hl': 'en'
    }

    # make the http GET request to Scale SERP
    http = urllib3.PoolManager()
    api_result = http.request('GET', 'https://api.scaleserp.com/search', fields=params)
    return json.loads(api_result.data.decode('utf-8'), parse_float=Decimal)


# takes a database item and returns the time since "tv" category as timedelta
def time_since_update(i):
    date_string = i["tv"]
    last_time = datetime.strptime(date_string, '%b %d %Y %I:%M')
    n = datetime.now()
    return n - last_time


# returns search result to use depending on table being accessed
def search_result(event):
    if event["table"] == "SearchResults":
        return places_by_name(
                        event['Q'],
                        event['L'],
                        event['P']
                    )
    else:
        return reviews_by_id(event["Id"])


# returns new item to use depending on table being accessed
def create_new_item(event):
    if event["table"] == "SearchResults":
        return {
                'Q': event['L'] + ':' + event['Q'],
                'P': event['P'],
                'tv': datetime.now().strftime('%b %d %Y %I:%M'),
                'results': places_by_name(
                            event['Q'],
                            event['L'],
                            event['P']
                            )
            }
    else:
        return {
                'Id': event["Id"],
                'tv': datetime.now().strftime('%b %d %Y %I:%M'),
                'results': reviews_by_id(event["Id"])
            }
            
            
# returns key to use depending on table being accessed            
def create_key(event):
    if event["table"] == "SearchResults":
        return {
                'Q': event['L'] + ':' + event['Q'],
                'P': event['P']
            }
    else:
        return {'Id': event["Id"]}
        

# event handler
def lambda_handler(event, context):
    # set values dependent on call parameters
    table = dynamodb.Table(event['table'])
    k = create_key(event)
    search = table.get_item(Key=k)

    # check and create or update item if needed
    if "Item" in search:
        if time_since_update(search["Item"]).days > time_limit:
            response = table.update_item(
                Key=k,
                UpdateExpression="set tv=:d, results=:r",
                ExpressionAttributeValues = {
                    ':d': datetime.now().strftime('%b %d %Y %I:%M'),
                    ':r': search_result(event)
                }
            )
    else:
        table.put_item(Item=create_new_item(event))

    return table.get_item(Key=k)["Item"]["results"]
