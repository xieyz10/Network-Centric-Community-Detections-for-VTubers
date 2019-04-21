import networkx as nx
import matplotlib.pyplot as plt
import math

graph = nx.read_gexf('../data/vtb.gexf')

nodeList = []
myNode = {
    "id": 0,
    "degree": 0,
    "weight": 0,
    "Jaccard": 0,
    "label": 0
}
centroids = []

def initialize(G, cluster):
    count = 0
    for node in graph:
        myNode["id"] = node
        myNode["degree"] = graph.degree(node)
        myNode["Jaccard"] = 0
        myNode["label"] = count%cluster
        count += 1
        nodeList.append(myNode.copy())

    for node, weight in G.degree(weight='weight'):
        try:
            nodeList[int(node)]["weight"] = weight
            # print(nodeList[int(node)])
        except:
            pass

    for i in range(cluster):
        centroids.append(nodeList[i])
        print(centroids)

    calculateJaccard(graph, cluster)
    return

def calculateJaccard(G, cluster):
    average = 0
    for node in nodeList:
        for center in centroids:
            preds = nx.jaccard_coefficient(G, [(node["id"], center["id"])])
            for u,v,p in preds:
                average += p
        average /= cluster
        node["Jaccard"] = average
        average = 0
        # print(node)
    return

def computeCentroid(cluster):
    newCentroid = {
        "degree": 0,
        "weight": 0,
        "Jaccard": 0,
        "label": 0,
        "numberOfNode": 0
    }
    temp = []
    for i in range(cluster):
        newCentroid["label"] = i
        temp.append(newCentroid.copy())

    for node in nodeList:
        temp[node["label"]]["degree"] += node["degree"]
        temp[node["label"]]["weight"] += node["weight"]
        temp[node["label"]]["numberOfNode"] += 1
        # print(temp)
    
    for i in range(cluster):
        temp[i]["degree"] = temp[i]["degree"]/temp[i]["numberOfNode"]
        temp[i]["weight"] = temp[i]["weight"]/temp[i]["numberOfNode"]
    return temp

def kmeans(G, cluster):
    minDist = 99999
    minLabel = 0
    changeLabel = False
    for node in nodeList:
        for center in centroids:
            dist = math.sqrt((node["degree"] - center["degree"])*(node["degree"] - center["degree"]) + (node["weight"] - center["weight"])*(node["weight"] - center["weight"]))
            if dist < minDist:
                minDist = dist
                minLabel = center["label"]
        if node["label"] != minLabel:
            changeLabel = True
        node["label"] = minLabel
        minDist = 99999
        minLabel = 0
        # print(node)
    return changeLabel

initialize(graph, 4)
calculateJaccard(graph, 4)
count = 1

while True:
    print("c=================================" + str(count) + "\n")
    count+=1
    result = kmeans(graph, 4)
    if result == False:
        break
    else:
        centroids = computeCentroid(4)
        for node in centroids:
            print(node)
    # for node in nodeList:
    #     print(node)

