import os
import logging
import requests
import json
from time import sleep
from datetime import datetime

log = logging.getLogger('airflow.task')

# Read Twitter API Token
def read_token():
    f = open('token.txt', 'r')
    token = f.read()
    f.close()

    return token

# Read last tweet ID
def read_since():
    since = open('since_id.txt', 'r')
    since_id = since.read()
    since.close()

    return since_id

# Save last downloaded tweet ID
def store_since(since_id):
    since = open('since_id.txt', 'w')
    since.write(since_id)
    since.close()

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
        raise Exception('Missing query argument')

    os.chdir(cwd)

    token = read_token()
    since_id = read_since()
    
    # Extended mode is needed in order to download tweets without being truncated
    querystring = '?q=' + query + '&result_type=recent&count=100&tweet_mode=extended&lang=en'

    log.info('Downloading first page of tweets..')
    tweets = send_request(querystring + '&since_id=' + since_id, token)

    while len(tweets['statuses']) > 0:
        store_file(tweets)

        # Find last tweet ID
        since_id = tweets['statuses'][-1]['id_str']
        store_since(since_id)

        # Sleep a bit just to avoid being blocked by twitter
        sleep(0.3)

        log.info('Downloading tweets since %s' % since_id)
        tweets = send_request(querystring + '&since_id=' + since_id, token)
        break

    log.info('Tweets download finished')
