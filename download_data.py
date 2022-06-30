import os
import logging as log
import requests
import json
from time import sleep
from datetime import datetime

# Read Twitter API Token
def read_token():
    f = open('token.txt', 'r')
    token = f.read()
    f.close()

    return token

# Save tweets to json file with datetime format
def store_file(tweets):
    with open('data/tweets-' + datetime.now().strftime("%Y%m%d%H%M%S") + '.json', 'w') as f:
        f.write(json.dumps(tweets['statuses']))

# Send tweets data request to Twitter API
def send_request(querystring, token):
    endpoint = 'https://api.twitter.com/1.1/search/tweets.json'
    url = endpoint + querystring
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers)
    
    if r.status_code >= 300:
        raise Exception('Error %d: %s' % (r.status_code, r.text))
    
    return r.json()

def download(query, cwd):
    if str(query).strip() == '':
        log.info('Cancelling since no query was provided')
        return

    os.chdir(cwd)

    token = read_token()
    
    # Extended mode is needed in order to download tweets without being truncated
    querystring = '?q=' + query + '&result_type=recent&count=100&tweet_mode=extended&lang=en'

    log.info('Downloading first page of tweets..')
    tweets = send_request(querystring, token)

    while len(tweets['statuses']) > 0:
        store_file(tweets)

        # Find last tweet ID
        since_id = tweets['statuses'][-1]['id_str']

        # Sleep a bit just to avoid being blocked by twitter
        sleep(0.3)

        log.info('Downloading tweets since %s' % since_id)
        tweets = send_request(querystring + '&since_id=' + since_id, token)
        break

    log.info('Tweets download finished')
