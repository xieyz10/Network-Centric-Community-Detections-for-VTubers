import networkx as nx
import matplotlib.pyplot as plt
import math

class Kmeans:
    #constructor
    def __init__(self, G, num_cluster):
        self.clusters = num_cluster
        self.graph = G
        self.nodeList = []
        self.centroids = []

    def initialize(self):
        count = 0
        tempNode = {
            "id": 0,
            "degree": 0,
            "weight": 0,
            "Jaccard": 0,
            "label": 0
        }
        
        for node in self.graph:
            tempNode["id"] = node
            tempNode["degree"] = self.graph.degree(node)
            tempNode["Jaccard"] = 0
            tempNode["label"] = count % self.clusters
            count += 1
            self.nodeList.append(tempNode.copy())

        for node, weight in self.graph.degree(weight='weight'):
            try:
                self.nodeList[int(node)]["weight"] = weight
                # print(self.nodeList[int(node)])
            except:
                pass

        for i in range(self.clusters):
            self.centroids.append(self.nodeList[i])
            print(self.centroids)
        
        return

    def calculateJaccard(self):
        average = 0
        for node in self.nodeList:
            for center in self.centroids:
                preds = nx.jaccard_coefficient(self.graph, [(node["id"], center["id"])])
                for u,v,p in preds:
                    average += p
            average /= self.clusters
            node["Jaccard"] = average
            average = 0
            # print(node)
        return

    def computeCentroid(self):
        newCentroid = {
            "degree": 0,
            "weight": 0,
            "Jaccard": 0,
            "label": 0,
            "numberOfNode": 0
        }
        temp = []
        for i in range(self.clusters):
            newCentroid["label"] = i
            temp.append(newCentroid.copy())

        for node in self.nodeList:
            temp[node["label"]]["degree"] += node["degree"]
            temp[node["label"]]["weight"] += node["weight"]
            temp[node["label"]]["numberOfNode"] += 1
            # print(temp)
        
        for i in range(self.clusters):
            temp[i]["degree"] = temp[i]["degree"]/temp[i]["numberOfNode"]
            temp[i]["weight"] = temp[i]["weight"]/temp[i]["numberOfNode"]

        self.centroids = []
        self.centroids = temp
        # for node in self.centroids:
        #     print(node)
        return

    def clustering(self):
        minDist = 99999
        minLabel = 0
        changeLabel = False
        for node in self.nodeList:
            for center in self.centroids:
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

    def printResult(self):
        for node in self.nodeList:
            print(node)

graph = nx.read_gexf('../data/vtb.gexf')
test = Kmeans(graph, 4)
test.initialize()
test.calculateJaccard()
count = 1
while True:
    print("=======================================================" + str(count) + "\n")
    count += 1
    result = test.clustering()
    print(result)
    if result == False:
        break
    else:
        test.computeCentroid()
    test.printResult()

