'''
this is the script to dectect all vtuber.
strictly, not all,  at most 200 vtuber will be saved to result.

This script will use BFS to search vtuber form a given "seed"

@Author Yihao Sun <stargazermiao@gmail.com>

'''

import twitter
import json
from util import try_until_success, load_config
from db import Mongo, UseCache

def bfsFinder():
    

if __name__ == "__main__":
    # load configure
    CONFIG = load_config()

    vtbSeed = CONFIG["twitter"]["seed"]
    vtbMaxNum = CONFIG["twitter"]["vtb_max"]
    mongoHost = CONFIG["mongo"]["addr"]
    authlist = CONFIG["twitter"]["auth"]

    twiAuthList = list(map(lambda a: twitter.oauth.OAuth(
        a["oauth_token"], a["oauth_token_secret"],
        a["consumer_key"], a["consumer_secret"]), authlist))

    twiList = list(map(lambda a: twitter.Twitter(auth=a), twiAuthList))

    db = Mongo(mongoHost, "twitter")
