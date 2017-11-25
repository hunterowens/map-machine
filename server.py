import requests
import flask
from dotenv import load_dotenv
import os
import random 
from bs4 import BeautifulSoup

import urllib.request
# OR, the same with increased verbosity:
load_dotenv('.env', verbose=True)

map_max = 13500;

mapurl_front = 'http://collections.lib.uwm.edu/digital/collection/agdm/id/'
mapurl_back = '/rec/4'
imgurl_front = 'http://collections.lib.uwm.edu/digital/download/collection/agdm/id/'
imgurl_back = '/size/medium'


from TwitterAPI import TwitterAPI

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def random_url():
    num = random.randint(1,map_max)
    return {'mapurl': mapurl_front + str(num) + mapurl_back,
            'imgurl': imgurl_front + str(num) + imgurl_back
            }

def get_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    meta = soup.find('meta', property="og:title") 
    title = meta.attrs['content']
    return title

def tweet(content, img_path): 
    data = urllib.request.urlopen(img_path)
    r = api.request('statuses/update_with_media', {'status':content}, {'media[]':data})
    return r.status_code

app = flask.Flask(__name__)

@app.route("/tweet")
def index():
    urls = random_url()
    title = get_title(urls['mapurl'])
    content = title + '  ' + urls['mapurl']
    tweet(content , urls['imgurl'])
    return "works"

if __name__ == '__main__':
    app.run()
