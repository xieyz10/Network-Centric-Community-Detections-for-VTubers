'''

this is the script for datasource vtuber-post
https://vtuber-post.com/database/

@Author Yihao Sun <stargazermiao@gmail.com>

'''

from http import cookiejar
from urllib import request
import json
from functools import reduce
import operator
import re
from bs4 import BeautifulSoup

DATA_SOURCE_HOST = "https://vtuber-post.com/database/"

cache = {}


def findAllVtbInPage(page):
    parent_node = page.find('div', class_='heightLineParent')
    vlist = []
    for vtb_nodes in parent_node.find_all('div', class_='clearfix'):
        vtb = {}
        name_node = vtb_nodes.find('p', class_='name')
        vtb['name'] = name_node.a.contents[0]
        vtb['detail_url'] = name_node.a['href']
        # get detail page
        with request.urlopen(DATA_SOURCE_HOST+vtb['detail_url']) as res:
            detail_page = BeautifulSoup(res.read())
            # info_node = detail_page.find('div', class_='vtuber_detail')
            twi_node = detail_page.find_all(
                'a', href=re.compile('twitter.com'))[1]
            twi_name = twi_node.contents[0]
            vtb['twi_name'] = twi_name
            print(twi_name)
        channel_node = vtb_nodes.find('p', class_='channel')
        vtb['channel'] = channel_node.a.contents[0]
        vtb['channel_url'] = channel_node.a['href']
        group_node = vtb_nodes.find('p', class_='group')
        try:
            vtb['group'] = group_node.a.contents[0]
            vtb['group_detail_url'] = group_node.a['href']
        except:
            vtb['group'] = ''
            vtb['group_detail_url'] = ''
        regist_node = vtb_nodes.find('p', 'regist')
        reg_str = regist_node.contents[0][0:-1]
        vtb['regsit'] = int(reg_str.replace(',', ''))
        play_node = vtb_nodes.find('p', 'play')
        play_str = play_node.contents[0][0:-1]
        vtb['play'] = int(play_str.replace(',', ''))
        upload_node = vtb_nodes.find('p', 'upload')
        upload_str = upload_node.contents[0][0:-1]
        vtb['upload'] = int(upload_str.replace(',', ''))
        vlist.append(vtb)
        # download thumbnil
        # thumb_node = vtb_nodes.find('img')
        # thumb_url = "../data/thumbnil/"+vtb['name'].replace('/', '_')+".jpg"
        # request.urlretrieve(thumb_node['src'], thumb_url)
    return vlist


def getAllVtber():
    # search_req = 'keyword=&startDate=&endDate=&office=&order=7&limit=100&collabo=&projects=&country=&non_movie=&fav=&colabo_genre_h=&customer_h=&prefectures_h=&genre_h=&model_h=&attribute_h=&creature_h=&job_h=&appearance_h=&searchFlg=0&page={0}&pageFlg=1'
    search_req = 'keyword=&startDate=&endDate=&office=&order=7&limit=25&collabo=&colabo_genre%5B%5D=&projects=&customer%5B%5D=&country=&prefectures%5B%5D=&genre%5B%5D=&model%5B%5D=&attribute%5B%5D=&creature%5B%5D=&job%5B%5D=&appearance%5B%5D=&submit=%E4%B8%8A%E8%A8%98%E3%81%AE%E6%9D%A1%E4%BB%B6%E3%81%A7%E7%B5%9E%E3%82%8A%E8%BE%BC%E3%82%80&searchFlg=0'
    req = request.Request(DATA_SOURCE_HOST, data=search_req.encode())
    jar = cookiejar.CookieJar()
    cookie_p = request.HTTPCookieProcessor(jar)
    opener = request.build_opener(cookie_p)
    with opener.open(req) as res:
        html_data = res.read()
        cache[search_req] = html_data
    root = BeautifulSoup(html_data)
    # get the vtb counts
    max_counts_node = root.find('p', class_='result')
    print(max_counts_node.strong.contents[0])
    max_counts_str = max_counts_node.strong.contents[0]
    max_counts = int(max_counts_str.replace(',', ''))
    page_num = max_counts // 100
    pages_content = []
    # get all pages
    search_req = 'keyword=&startDate=&endDate=&office=&order=7&limit=100&collabo=&projects=&country=&non_movie=1&fav=&colabo_genre_h=&customer_h=&prefectures_h=&genre_h=&model_h=&attribute_h=&creature_h=&job_h=&appearance_h=&searchFlg=0&page={}&pageFlg=1'
    for p in range(10):
        req = request.Request(
            DATA_SOURCE_HOST, data=search_req.format(p).encode())
        with opener.open(req) as res:
            html_data = res.read()
            # cache[search_req] = html_data
            pages_content.append(BeautifulSoup(html_data))
    vtbs = list(
        reduce(operator.add, (map(lambda p: findAllVtbInPage(p), pages_content))))
    # save to  file
    with open('../data/vtuber.json', 'w+') as out:
        out.write(json.dumps(vtbs, ensure_ascii=False))


if __name__ == "__main__":
    getAllVtber()
