'''
this is script used to create vtuber network

at this time, co-live and times will be used as edge weight of

'''
import re
import random
import math

import networkx
import matplotlib.pyplot as plt

from db import Mongo
from util import load_config

CONFIG = load_config()

CHANNEL_URL = [
    r'youtube.com/c/[a-zA-Z\d_-]+',
    r'youtube.com/channel/[a-zA-Z\d_-]+',
    r'youtube.com/user/[a-zA-Z\d_-]+']
CHANNEL_URL = list(map(re.compile, CHANNEL_URL))

node_count = 0
# here is just some fake data for test


def sigmoid(x):
    '''
    sigmoid function to give a logistic like dist
    '''
    print(1 / (1 + math.exp(-x)))
    return 1 / (1 + math.exp(-x))


def gen_mock_data():
    '''
    generate fake data for test
    '''
    client = Mongo(CONFIG["mongo"]["addr"], 'youtube')
    data = client.loadWholeDoc('vtuber')
    graph = networkx.Graph()
    vtubers = []
    for i in range(10):
        vtubers.append(data[i]['channel'])
        graph.add_node(data[i]['channel'], viz={}, mod=1, id=0)
    pos = networkx.random_layout(graph)
    counter = 0
    for v in vtubers:
        graph.node[v]['id'] = counter
        graph.node[v]['viz']['size'] = 20
        graph.node[v]['viz']['position'] = {
            'x': pos[v][0] * (-100), 'y': pos[v][1] * 100, 'z': 0}
        graph.node[v]["viz"]['color'] = {'r': 255, 'g': 192, 'b': 201, 'a': 1}
        print(graph.node[v])
        counter = counter + 1

    graph.add_weighted_edges_from([
        (vtubers[1], vtubers[5], 3),
        (vtubers[2], vtubers[4], 2),
        (vtubers[1], vtubers[3], 3),
        (vtubers[1], vtubers[7], 1),
        (vtubers[5], vtubers[9], 3),
        (vtubers[4], vtubers[8], 3),
        (vtubers[1], vtubers[8], 3),
        (vtubers[1], vtubers[2], 3),
        (vtubers[6], vtubers[7], 2)
    ])
    #graph = networkx.generate_gexf(graph)
    # regen id
    networkx.write_gexf(graph, '../data/mock.gexf')


def add_node(channel, graph):
    global node_count
    if not graph.has_node(channel):
        graph.add_node(channel, viz={}, mod=-1, id=0)
        graph.node[channel]['id'] = node_count
        graph.node[channel]['viz']['size'] = 20
        graph.node[channel]["viz"]['color'] = {
            'r': 255, 'g': 192, 'b': 201, 'a': 1}
        node_count += 1


def extract_relation(owner_channel, desc, graph):
    '''
    extract channel id in the description of a video
    and then if it is a known vtuber, this will be consdered
    as a close relation between two exist vtuber

    for performance reason this graph is not filtered here
    (most of them should be in vtber list exist if not, just
    leave it)
    '''
    found_chanel = []
    for _p in CHANNEL_URL:
        tmp = _p.findall(desc)
        if tmp is not None:
            tmp = list(map(lambda s: s.split('/')[-1], tmp))
            found_chanel += tmp
    print(found_chanel)
    # add node&edges to graph
    add_node(owner_channel, graph)
    for _c in found_chanel:
        if _c is not owner_channel:
            add_node(_c, graph)
            if graph.has_edge(_c, owner_channel):
                # edge exist then just add weight
                graph.edges[_c, owner_channel]['weight'] += 1
            else:
                graph.add_weighted_edges_from(
                    [(_c, owner_channel, 1)])


def create_graph():
    '''
    create a vtuber relationd graph
    '''
    PAGE_SIZE = 20
    vgraph = networkx.Graph()
    client = Mongo(CONFIG["mongo"]["addr"], 'youtube')
    vtubers = client.loadWholeDoc('vtuber')
    video_num = client.loadWholeDoc('videosv2').count()
    for i in range(0, video_num, PAGE_SIZE):
        v_page = client.loadWholeDoc('videosv2').skip(i).limit(PAGE_SIZE)
        for v in v_page:
            owner = v['channelId']
            try:
                desc = v['description']
            except KeyError:
                # some times des is not exist in video
                continue
            extract_relation(owner, desc, vgraph)
    # preview
    # networkx.draw(vgraph, with_labels=True, font_weight='bold')
    # plt.show()
    # split the name from vtb list
    name_dict = {}
    vtb_dict = {}
    for v in vtubers:
        name = v['channel']
        try:
            channel_id = v['channel_url'].split('/')[-1]
        except:
            continue
        name_dict[channel_id] = name
        vtb_dict[channel_id] = v

    # update the position and size of node in graph
    pos = networkx.random_layout(vgraph)

    # clean out all node who is not in vtuber list
    remove_list = []
    for _n in vgraph.nodes():
        if not _n in name_dict.keys():
            remove_list.append(_n)
    vgraph.remove_nodes_from(remove_list)

    for _n in vgraph.nodes():
        vgraph.node[_n]['viz']['position'] = {
            'x': pos[_n][0] * (-100) * 1.5,
            'y': pos[_n][1] * 100, 'z': 0
        }
        # print(math.log2(vtb_dict[_n]['regsit']))
        #vgraph.node[_n]['viz']['size'] = vgraph.degree[_n]
        vgraph.node[_n]['viz']['size'] = (
            math.log2(vtb_dict[_n]['regsit'])-10)*10
    vgraph = networkx.relabel_nodes(vgraph, name_dict)
    # networkx.write_gexf(vgraph, '../data/vtb.gexf')
    return vgraph


def max_clique_graph(vgraph):
    print("total number of node is " + str(len(vgraph.node)))
    cliques = networkx.find_cliques(vgraph)
    # color all node into different
    mod = 0
    for clik in cliques:

        if len(clik) < 12:
            continue
        print(clik)
        _r = random.randint(0, 255)
        _g = random.randint(0, 255)
        _b = random.randint(0, 255)
        for _n in clik:
            vgraph.node[_n]['mod'] = mod
            vgraph.node[_n]["viz"]['color'] = {
                'r': _r, 'g': _g, 'b': _b, '1': 1}
        mod += 1
    print("total clique is " + str(mod))


if __name__ == "__main__":
    vgraph = create_graph()
    max_clique_graph(vgraph)
    networkx.write_gexf(vgraph, '../data/Max-Clique.gexf')
