'''
this script is use for collect data on https://mamedaifuku.sakura.ne.jp/

'''
import re
from urllib import request
import json
import bs4
from db import Mongo, UseCache
from util import load_config

CONFIG = load_config()

COMMENT_URL_BASE = 'https://mamedaifuku.sakura.ne.jp/live_stream/php/ex_disp_message.php?v={}&disp_message_info_mode=2&disp_message_author_mode=1&disp_message_comment_mode=1&ym=&turning_page_mode=true&message_page=1'

COMMENT_FANS = "commFans"
database = Mongo(CONFIG["mongo"]["addr"], 'youtube')


def get_video_list():
    '''
    fecth all video from all users
    '''
    with request.urlopen('https://mamedaifuku.sakura.ne.jp/live_stream/php/ex_return_video_list_json.php?get_video_list_mode=all') as res:
        # with open('../data/video.json', 'w+') as tmp:
            # tmp.write(res.read().decode())
        # database = Mongo(CONFIG["mongo"]["addr"], 'youtube')
        data = res.read().decode()
        # print(data)
        database.saveBulkToDoc('videosv2', json.loads(data))


@UseCache(db=database, keyword='video_id')
def extract_commenter(video_id):
    '''
    Given the id of a video
    extract the name list of comment from a ex_info page of
    mamedaifuku, these are people who join in this video's
    live chat
    '''
    fans_name = set()
    with request.urlopen(COMMENT_URL_BASE.format(video_id)) as res:
        # parse html
        comment_page = bs4.BeautifulSoup(res.read())
        try:
            comment_tabel = comment_page.find_all('table')[1]
            fans = comment_tabel.find_all(
                'a', href=re.compile('mamedaifuku.sakura.ne.jp/'))
            for n in fans:
                if len(n.contents) is not 0:
                    fans_name.add(n.contents[0])
                    print(n.contents[0])
        except:
            print(comment_page)
            pass
    return fans_name


def get_all_fans_of_all_vtb():
    '''
    get all the fans form 5 latest live of a vtuber
    '''
    vtbs = database.loadWholeDoc('vtuber')
    for v in vtbs:
        videos = database.lookup('videosv2', {'channelTitle': v['channel']}, 5)
        fans_name = set()
        for video in videos:
            # fetch fans from data source
            print(video)
            fans_name = fans_name | extract_commenter(video['videoId'])
        # save to database
        channel_id = v['channel_url'].split('/')[-1]
        fan_list = list(fans_name)
        print(len(fan_list))
        if len(fan_list) is not 0:
            database.saveOneToDoc(COMMENT_FANS, {
                'channelName': v['channel'],
                'channelId': channel_id,
                'fans': fan_list
            })


if __name__ == "__main__":
    get_all_fans_of_all_vtb()
