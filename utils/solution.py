from itertools import combinations
import numpy as np
import networkx as nx
from copy import deepcopy


def findRadiusPoint(cluster, distanceMatrix):
    # minPoint = min(cluster, key=lambda point: distanceMatrix[storehouse, point])
    # return distanceMatrix[minPoint, storehouse]
    maxDistance = 0
    points = []
    for pairOfPoint in combinations(cluster, 2):

        distance = distanceMatrix[pairOfPoint[0],
                                  pairOfPoint[1]]
        if maxDistance < distance:
            maxDistance = distance
            points = pairOfPoint
    return points


def findMax(cluster, distanceMatrix):
    maxDistance = 0
    for pairOfPoint in combinations(cluster, 2):
        distance = distanceMatrix[pairOfPoint[0],
                                  pairOfPoint[1]]
        if maxDistance < distance:
            maxDistance = distance
    return maxDistance


def getRadius(clusterList, distanceMatrix):
    radiusList = []
    for cluster in clusterList:
        radiusList.append(findMax(cluster, distanceMatrix))
    return radiusList


def getInfo(cluster, weightClusterSolution, weightOfVehicle, distanceMatrix):
    info = []
    storehouse = len(distanceMatrix) - 1
    info.append(weightClusterSolution)
    info.append(weightOfVehicle)
    info.append(findMax(cluster, distanceMatrix))
    info.append(MST(cluster, distanceMatrix))
    info.append(minDisPointToCluster(storehouse, cluster, distanceMatrix))
    return info

def MST(points, distanceMatrix):
    # find MST by Prim
    cost = 0
    candidatePoint = points.copy()
    n = len(points)
    selected_vertices = set([candidatePoint.pop(0)])
    mst = []  
    while len(selected_vertices) < n:
        candidate_edges = []
        for vertex in selected_vertices:
            for point in candidatePoint:
                if point not in selected_vertices:
                    candidate_edges.append((vertex, point, distanceMatrix[vertex][point]))

        min_edge = min(candidate_edges, key=lambda x: x[2])
        candidatePoint.remove(min_edge[1])
        selected_vertices.add(min_edge[1])
        mst.append(min_edge)
        cost += min_edge[2]
    return cost
   

def minDisPointToCluster(point, cluster, distanceMatrix):
    minPoint = min(
        cluster, key=lambda point: distanceMatrix[point, point])
    return distanceMatrix[minPoint, point]

def getCost(cluster):
    return cluster[0] * cluster[1] * cluster[2] * (cluster[3] + cluster[4])


def costFuction(infoClusters):
    totalCost = 0
    for cluster in infoClusters:
        totalCost += getCost(cluster)
    return totalCost


class Solution:
    """
    Contains a list of customers, weight list and distance matrix 
    """
    # costFuction = weightCluster*weightOfVehicle*radius*(MST + distanceToStorehouse)
    # [{weightCluster: 0}, {weightOfVehicle: 1}, {radius: 2}, {MST: 3}, {distanceToStorehouse: 4}]

    def __init__(self, solutionList, weightClusterSolution, distanceMatrix, dataModel):
        self.dataModel = dataModel
        self.solutionList = solutionList
        self.infoClusters = [getInfo(solutionList[idxCluster],
                                     weightClusterSolution[idxCluster],
                                     dataModel.weightOfVehicle[idxCluster],
                                     distanceMatrix)
                             for idxCluster in range(len(solutionList))]
        self.costFuction = costFuction(self.infoClusters)

    def __copy__(self):
        return self.__class__(deepcopy(self.solutionList), self.weightClusterSolution,
                              self.distanceMatrix)
