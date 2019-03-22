'''
this is a mongodb util
following utility included:
- a connection manager **class Mongo**
- **UseCache** can be used to check cache before request

it will cache the data according to function signature
if a single collection is too large it will be split into
several documents

NOTICE: the maxium document size of mongodb is 14MB, if data
or key is too large plz split it or use gridfs

TODO: use grid fs to store, cause profile many very large!
      for some application (eg. get all friends profile).


@Author Yihao Sun <stargazermiao@gmail.com>

'''
import pymongo
from pymongo import MongoClient
# import gridfs

MAX_BSON_SIZE = 800000


class Mongo:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client[db]
        self.cacheDb = self.client['cache']

    def saveToCache(self, req, data, key=None):
        doc = self.cacheDb[req]
        try:
            doc.insert_one({'key': key, 'data': data})
        except Exception as e:
            print(e)

    def checkCache(self, req, key):
        doc = self.cacheDb[req]
        data = doc.find_one({'key': key})
        return data


class UseCache(object):
    '''
    an decorator check whether a request is already cached
    this will decrease the request frequency because twitter
    limit the requset number per time window 

    keyword is the key argument name in sign of targer function
    default key is the last one of arg list.
    if key is not found in kwargs, default value will be used.

    eg: 
    @UseCache(db, keyword)
    getFollowerIds(.....)
    '''

    def __init__(self, db, keyword):
        self.db = db
        self.keyword = keyword

    def __call__(self, func):
        '''
        the wrapper for function who want to check if
        this function call is already cached, each different
        function requets call is stored in a mongodb document
        '''
        def wrapper(*args, **kwargs):
            req = func.__name__
            data = None
            if self.keyword in kwargs.keys():
                key = kwargs[self.keyword]
            else:
                key = args[-1]

            found = self.db.checkCache(req, key)
            if found is not None:
                data = found['data']

            if data is None:
                # cache miss
                # print(screen_name + str(uid) + " miss")
                data = func(*args, **kwargs)
                self.db.saveToCache(req, data, key)

            assert(data is not None)
            return data
        return wrapper
