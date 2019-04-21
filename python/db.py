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

NOTE: use grid fs to store, cause profile many very large!
      for some application (eg. get all friends profile).


@Author Yihao Sun <stargazermiao@gmail.com>

'''
from functools import wraps
from pymongo import MongoClient
# import gridfs

MAX_BSON_SIZE = 800000


class Mongo:
    '''
    abstract class for database operation
    '''

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

    def saveBulkToDoc(self, doc_name, data):
        self.db[doc_name].insert_many(data)

    def saveOneToDoc(self, doc_name, data):
        self.db[doc_name].insert_one(data)

    def updateOne(self, doc_name, query, change):
        self.db[doc_name].find_one_and_update(
            query,
            {'$set': change}
        )

    def lookup(self, collection_name, query, limit=100):
        '''
        seach for data in database, with a given limitation
        '''
        return self.db[collection_name].find(query).limit(limit)
    # def aggregate(self, doc_name, query):
    #     self.db

    def loadWholeDoc(self, doc_name):
        '''
        this will return all data in a mongodb collection
        plz catch exception for doc dose not exists
        '''
        return self.db[doc_name].find()

    def loadOne(self, doc_name, q):
        return self.db[doc_name].find_one(q)

    def cacheDrop(self):
        '''
        clean the cache
        this should be called periodicaly
        '''
        self.cacheDb.drop()


class UseCache:
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

    def __init__(self, db=None, keyword=None):
        self.db = db
        self.keyword = keyword

    def __call__(self, func):
        '''
        the wrapper for function who want to check if
        this function call is already cached, each different
        function requets call is stored in a mongodb document
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.db is None:
                return func(*args, **kwargs)
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
            return data
        return wrapper


def cache(db):
    '''
    this is basicly a currify version of UsedCache, cause python do
    not support currify
    '''
    def cons_key(keyword):
        def cons_func(func):
            def wrapper(*args, **kwargs):
                req = func.__name__
                data = None
                if keyword in kwargs.keys():
                    key = kwargs[keyword]
                else:
                    key = args[-1]

                found = db.checkCache(req, key)
                if found is not None:
                    data = found['data']

                if data is None:
                    # cache miss
                    # print(screen_name + str(uid) + " miss")
                    data = func(*args, **kwargs)
                    db.saveToCache(req, data, key)
                return data
            return wrapper
        return cons_func
    return cons_key
