'''
this script is use for collect data on https://mamedaifuku.sakura.ne.jp/

'''
from urllib import request
import json
from db import Mongo

from util import load_config

CONFIG = load_config()
with request.urlopen('https://mamedaifuku.sakura.ne.jp/live_stream/php/ex_return_video_list_json.php?get_video_list_mode=all') as res:
    # with open('../data/video.json', 'w+') as tmp:
        # tmp.write(res.read().decode())
    database = Mongo(CONFIG["mongo"]["addr"], 'youtube')
    data = res.read().decode()
    # print(data)
    database.saveBulkToDoc('videosv2', json.loads(data))
