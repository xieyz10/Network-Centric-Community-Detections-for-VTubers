'''
this script is used to retrive all youtube related thing
form youtube api.

I also want to get data on live chat replay, but it can't
be done in api way, a scrapy is exactly needed, in future
it should be added

@Author Yihao Sun <stargazermiao@gmail.com>
'''
import time
import json

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from db import Mongo,UseCache
from util import load_config

CONFIG = load_config()

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_SECRETS_FILE = "client_secret_405709008166-k5os3m7treou9nbbqos796upceqe2pm8.apps.googleusercontent.com.json"
DATABASE = Mongo(CONFIG["mongo"]["addr"], 'youtube')
class YouTube:
    '''
    this is the manager entity for  youtube api operation
    '''
    _db = None

    def __init__(self, secret):
        # get OAuth2 credential info
        # self._db = database
        flow = InstalledAppFlow.from_client_secrets_file(secret, SCOPES)
        credentials = flow.run_local_server()
        self.service = build(API_SERVICE_NAME, API_VERSION,
                             credentials=credentials)

    @UseCache(db=DATABASE, keyword='chan_id')
    def get_channel_videos(self, chan_id):
        '''
        get all video of a channel with given channel id
        '''
        # pylint: disable=maybe-no-member
        result = []
        response = self.service.search().list(
            part='snippet',
            channelId=chan_id,
            maxResults=50,
            type='video'
        ).execute()
        result = result + response['items']
        while 'nextPageToken' in response.keys():
            response = self.service.search().list(
                part='snippet',
                channelId=chan_id,
                maxResults=50,
                pageToken=response['nextPageToken'],
                type='video'
            ).execute()
            res_info = response['pageInfo']
            result = result + response['items']
        return result

    #@UseCache(db=DATABASE, keyword='video_id')
    def get_video_detail(self, video_id):
        '''
        get the detail of a video, the snippet is not
        enough, a full description will be useful to
        analysis
        '''
        part = 'snippet,statistics,topicDetails'
        # pylint: disable=maybe-no-member
        response = self.service.videos().list(
            part=part,
            id=video_id).execute()
        return response['items']

    def search_live(self, channel_id):
        '''
        this function is used to seacrch whether a
        channel is live now, if not a None will return
        '''
        # pylint: disable=maybe-no-member
        # get live id
        search_res = self.service.search().list(
            part='snippet',
            eventType='live',
            maxResults=25,
            channelId=channel_id,
            type='video').execute()
        if search_res is not None:
            live_info = self.service.videos().list(
                part='snippet,statistics,topicDetails',
                id=search_res['item'][0]['id']['video_id']
            ).execute()
            return live_info
        return None

# def extract_id_from_snippt(video):


if __name__ == "__main__":
    CLIENT = YouTube(CLIENT_SECRETS_FILE)
    # read all vtuber data in
    with open('../data/vtuber.json') as vtb_file:
        data = vtb_file.read()
        vtbs = json.loads(data)[:500]
    # update the vtuber info in data base
    # DATABASE.saveBulkToDoc('vtuber', vtbs)
    # get the page of each vtuber
    for v in vtbs:
        channel_url = v['channel_url']
        chan_id = channel_url.split('/')[-1]
        video_snippt = CLIENT.get_channel_videos(chan_id)
        ids = []
        for v in video_snippt:
            try:
                ids.append(v['id']['videoId'])
            except:
                print(v)
        time.sleep(60)
        # fectch the detail of each videos page by page
        print(ids)
        videos = []
        for i in range(0, len(video_snippt), 50):
            ids_str = ','.join(ids[i: i+25])
            res = CLIENT.get_video_detail(ids)
            videos = videos + res
        # persist to data base
        print(videos)
        time.sleep(60)
        DATABASE.saveOneToDoc(
            'videos', {'channel_id': chan_id, 'data': videos})
