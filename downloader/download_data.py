import os
import sys
import logging as log
import requests
import json
from time import sleep
from datetime import datetime

# Save tweets to json file with datetime format
def store_file(tweets):
    with open('/shared/tweets_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.json', 'w') as f:
        f.write(json.dumps(tweets['statuses']))

# Send tweets data request to Twitter API
def send_request(querystring):
    endpoint = 'https://api.twitter.com/1.1/search/tweets.json'
    url = endpoint + querystring
    headers = {'Authorization': 'Bearer ' + os.getenv('TW_TOKEN', '')}
    r = requests.get(url, headers=headers)
    
    if r.status_code >= 300:
        raise Exception('Error %d: %s' % (r.status_code, r.text))
    
    return r.json()

def find_last_file():
    directory = '/shared/'
    prefix = 'genericspider_'

    newest_date = 0
    newest_file = ''
    files = os.listdir(directory)
    log.info('Files found on dir: %d' % len(files))
    for file in files:
        if not prefix in file:
            continue

        file_date = int(file.replace(prefix, ''))
        if file_date > newest_date:
            newest_date = file_date
            newest_file = prefix + str(newest_date)

    return directory + newest_file

if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    
    query = ''
    last_file = find_last_file()
    with open(last_file, 'r') as search_file:
        last_search = json.loads(search_file.read())
        query = last_search['search'] if 'search' in last_search else ''

        log.info('Founded on file: %s' % query)

    if str(query).strip() == '':
        log.info('Cancelling since no query was provided')
        exit(1)
    
    # Extended mode is needed in order to download tweets without being truncated
    querystring = '?q=' + query + '&result_type=recent&count=100&tweet_mode=extended&lang=en'

    log.info('Downloading first page of tweets..')
    tweets = send_request(querystring)

    while len(tweets['statuses']) > 0:
        store_file(tweets)

        # Find last tweet ID
        since_id = tweets['statuses'][-1]['id_str']

        # Sleep a bit just to avoid being blocked by twitter
        sleep(0.3)

        log.info('Downloading tweets since %s' % since_id)
        tweets = send_request(querystring + '&since_id=' + since_id)

    log.info('Tweets download finished')
