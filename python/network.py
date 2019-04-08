'''
this is script used to create vtuber network

at this time, co-live and times will be used as edge weight of

'''
import json

import networkx

from db import Mongo
from util import load_config

CONFIG = load_config()

# here is just some fake data for test


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
        graph.node[v]["viz"]['color'] = {'r': 0, 'g': 0, 'b': 255, 'a': 0}
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


gen_mock_data()
