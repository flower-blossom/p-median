from itertools import combinations
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


def MST(cluster, matrix):
    G = nx.Graph()
    for i in range(len(cluster)):
        firstPoint = cluster[i]
        G.add_node(firstPoint)
        for j in range(i+1, len(cluster)):
            secondPoint = cluster[j]
            G.add_edge(firstPoint, secondPoint, weight=matrix[firstPoint][secondPoint])
    MST = nx.minimum_spanning_tree(G)

    length = sum([MST[u][v]['weight'] for u, v in MST.edges()])

    return length    

def distanceToStorehouse(storehouse, cluster, distanceMatrix):
    minPoint = min(cluster, key=lambda point: distanceMatrix[storehouse, point])
    return distanceMatrix[minPoint, storehouse]


def costFuction(solution, dataModel, radiusClusters):
    solutionList = solution.solutionList
    quantityOfCluster = len(solutionList)
    weightClusterSolution = solution.weightClusterSolution
    distanceMatrix = solution.distanceMatrix
    weightOfVehicle = dataModel.weightOfVehicle
    storehouse = len(distanceMatrix)
    totalCost = 0

    for idxCluster in range(quantityOfCluster):
        totalCost += weightClusterSolution[idxCluster] * \
                        weightOfVehicle[idxCluster] * \
                        MST(solutionList[idxCluster], distanceMatrix) * \
                        radiusClusters[idxCluster]
                        
        totalCost += 2 * distanceToStorehouse(storehouse, 
                                              solutionList[idxCluster], 
                                              distanceMatrix)

    return totalCost


class Solution:
    """
    Contains a list of customers, weight list and distance matrix 
    """
    # costFuction = weightCluster*weightOfVehicle*MST + 2*distanceToStorehouse
    # [{weightCluster}, {weightOfVehicle}, {MST}, {distanceToStorehouse}]
    def __init__(self, solutionList, weightClusterSolution, distanceMatrix, dataModel):
        self.dataModel = dataModel
        self.solutionList = solutionList
        self.weightClusterSolution = weightClusterSolution
        self.distanceMatrix = distanceMatrix
        self.radiusClusters = getRadius(
            self.solutionList, self.distanceMatrix)
        self.totalDistance = sum(self.radiusClusters)
        self.costFuction = costFuction(solutionList, dataModel, self.radiusClusters)

    def __copy__(self):
        return self.__class__(deepcopy(self.solutionList), self.weightClusterSolution,
                              self.distanceMatrix)
