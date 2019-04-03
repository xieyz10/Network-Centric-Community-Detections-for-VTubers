'''
this script is used to retrive all youtube related thing
form youtube api.

I also want to get data on live chat replay, but it can't
be done in api way, a scrapy is exactly needed, in future
it should be added

@Author Yihao Sun <stargazermiao@gmail.com>
'''
from functools import partial

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from db import Mongo, UseCache
from util import load_config

CONFIG = load_config()

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_SECRETS_FILE = "../client_secret_974874009372-ssl9fmjep6jvu6sur8nbeqea6mv2hpbu.apps.googleusercontent.com.json"


class YouTube:
    '''
    this is the manager entity for  youtube api operation
    '''
    _db = None

    def __init__(self, secret):
        # get OAuth2 credential info
        # self._db = database
        flow = InstalledAppFlow.from_client_secrets_file(secret, SCOPES)
        credentials = flow.run_console()
        self.service = build(API_SERVICE_NAME, API_VERSION,
                             credentials=credentials)

    def get_channel_videos(self, chan_id):
        '''
        get all video of a channel with given channel id
        '''
        # pylint: disable=maybe-no-member
        result = []
        response = self.service.search().list(
            part='snippet',
            channelId=chan_id,
            maxResults=50
        ).execute()
        res_info = response['page_info']
        result = result + response['items']
        while 'nextPageToken' in res_info.keys():
            response = self.service.search().list(
                part='snippet',
                channelId=chan_id,
                maxResults=50,
                pageToken=res_info['nextPageToken']
            ).execute()
            res_info = response['page_info']
            result = result + response['items']
        return result

    # @UseCache(db=db, keyword='video_id')
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
        return response

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
