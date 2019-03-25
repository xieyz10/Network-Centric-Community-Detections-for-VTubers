'''
this is the script to dectect all vtuber.
strictly, not all,  at most 200 vtuber will be saved to result.

This script will use BFS to search vtuber form a given "seed"

@Author Yihao Sun <stargazermiao@gmail.com>

'''
from sys import maxsize as maxint
import json
import urllib.request

import twitter

from util import try_until_success, load_config
from db import Mongo, UseCache

CONFIG = load_config()

vtbSeed = CONFIG["twitter"]["seed"]
vtbMaxNum = CONFIG["twitter"]["vtb_max"]
mongoHost = CONFIG["mongo"]["addr"]
authlist = CONFIG["twitter"]["auth"]

twiAuthList = list(map(lambda a: twitter.oauth.OAuth(
    a["oauth_token"], a["oauth_token_secret"],
    a["consumer_key"], a["consumer_secret"]), authlist))

special = ['914724274274832384', '803480007775383552', '1019885045933211648', '984028782175629314']
black = [746964642660966403]

twiList = list(map(lambda a: twitter.Twitter(auth=a), twiAuthList))
db = Mongo(mongoHost, "twitter")


class UserNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return(repr(self.value) + ' is not found.')


@UseCache(db=db, keyword='user_id')
def getUserProfile(apilist, user_id=''):
    '''
    get the profile of a user with given screen_name
    '''
    def helper():
        res = None
        for api in apilist:
            try:
                res = api.users.show(user_id=user_id, cursor=-1)
                break
            except Exception:
                pass
        if res is None:
            raise UserNotFoundException(user_id)
        return res
    res = try_until_success(helper)
    return res


@UseCache(db=db, keyword="user_id")
def getFriendId(apilist, user_id=None, limit=maxint):
    '''
    get all followers page by page
    This is most time consuming function call
    '''
    friends = []
    cursor = -1

    while cursor != 0:
        def helper():
            res = None
            for api in apilist:
                try:
                    res = api.friends.ids(
                        user_id=user_id, cursor=cursor, count=limit)
                    break
                except Exception:
                    pass
            if res is None:
                raise UserNotFoundException(user_id)
            return res
        data = try_until_success(helper)
        friends = friends + data['ids']
        cursor = data['next_cursor']
    return friends


@UseCache(db=db, keyword="user_id")
def getBulkUserProfilePage(apilist, user_id=None):
    data = []

    def helper():
        res = None
        for api in apilist:
            try:
                res = api.users.lookup(user_id=user_id, cursor=-1)
                break
            except Exception:
                pass
        if res is None:
            raise UserNotFoundException(user_id)
        return res
    data = try_until_success(helper)
    return data


def getBulkUserProfile(apilist, user_id=[]):
    '''
    get mutiple user profiles at a time
    '''
    data = []
    user_id = list(map(str, user_id))
    for i in range(0, len(user_id), 100):
        req_str = ','.join(user_id[i: i+100])
        data = data + getBulkUserProfilePage(apilist, user_id=req_str)
    return data


def isVtuber(profile):
    '''
    only vtuber has more than 15000 fans can be dectected
    '''
    if profile['id'] in black:
        return False
    if profile['followers_count'] < 15000:
        return False
    if profile['description'].lower().find('pixiv') > 0:
        return False
    channel_uri = "youtube.com/channel"
    if profile['description'].lower().find('vtuber') > 0:
        return True
    if profile['description'].lower().find('virtual youtuber') > 0:
        return True
    if profile['description'].lower().find('漫画家') > 0:
        return False
    if profile['description'].lower().find('goo.gl/') > 0:
        return True
    # if str(profile['description'].find('VTuber')) > 0:
    #     return True
    # if profile['description'].lower().find('Youtuber') > 0:
    #     return True
    if str(profile['entities']).find(channel_uri) > 0:
        return True
    else:
        return False

def sortUserByFollowers(users, count):
    if count is -1:
        return sorted(users, key=lambda u: u['followers_count'], reverse=True)
    return sorted(users, key=lambda u: u['followers_count'])[:count]

def bfsFinder(seed, vtbMaxNum):
    print("seed is " + str(seed))
    visited = []
    tmp = [seed]
    result = {}
    result[seed] = getUserProfile(twiList, user_id=seed)
    for s in special:
        result[s] = getUserProfile(twiList, user_id=s)
    next_level = []
    count = 1
    while count < vtbMaxNum:
        if len(tmp) is 0:
            tmp = tmp + next_level
            next_level.clear()
        uid = tmp.pop()
        if uid in visited:
            continue
        visited.append(uid)
        friends_id = getFriendId(twiList, user_id=uid)
        friends_profile = getBulkUserProfile(twiList, friends_id)
        for p in friends_profile:
            if isVtuber(p):
                result[p['id']] = p
                count = count + 1
                next_level.append(p['id'])
                
    return result


if __name__ == "__main__":
    # load configure
    vtbs = bfsFinder(vtbSeed, vtbMaxNum)
    with open("../data/vtuber.json", "w+") as out:
        vtbs = sortUserByFollowers(vtbs.values(), 500)
        # for p in vtbs:
        #     try:
        #         urllib.request.urlretrieve(
        #             p['profile_image_url'], 
        #             "../data/img/"+p["screen_name"].replace('noraml', 'bigger')+".jpg")
        #     except:
        #         pass
        out.write(json.dumps(vtbs, ensure_ascii=False))
