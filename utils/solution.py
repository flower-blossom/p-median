from itertools import combinations
from typing import List, Tuple, Type
import numpy as np
from copy import deepcopy
from alns import State

def getMaxRadius(cluster, distanceMatrix):
    maxDistance = 0
    for pairOfPoint in combinations(cluster, 2):
        distance = distanceMatrix[pairOfPoint[0],
                                  pairOfPoint[1]]
        if maxDistance < distance:
            maxDistance = distance
    return maxDistance


def getInfo(cluster, weightClusterSolution, weightOfVehicle, distanceMatrix, depot):
    # Get infomation of problem
    info = []
    info.append(weightClusterSolution)
    info.append(weightOfVehicle)
    info.append(getMaxRadius(cluster, distanceMatrix))
    info.append(MST(cluster, distanceMatrix)[0])
    info.append(minDisPointToCluster(depot, cluster, distanceMatrix))
    return info


def MST(points, distanceMatrix):
    # find MST distance by Prim
    cost = 0
    candidatePoint = points.copy()
    n = len(points)
    selected_vertices = set([candidatePoint.pop(0)])
    mst = []
    egdesMST = []
    while len(selected_vertices) < n:
        candidate_edges = []
        for vertex in selected_vertices:
            for point in candidatePoint:
                if point not in selected_vertices:
                    candidate_edges.append(
                        (vertex, point, distanceMatrix[vertex][point]))

        min_edge = min(candidate_edges, key=lambda x: x[2])
        egdesMST.append(min_edge)
        candidatePoint.remove(min_edge[1])
        selected_vertices.add(min_edge[1])
        mst.append(min_edge)
        cost += min_edge[2]
    return cost, egdesMST


def minDisPointToCluster(point, cluster, distanceMatrix):
    minPoint = min(
        cluster, key=lambda secondPoint: distanceMatrix[point, secondPoint])
    return distanceMatrix[minPoint, point]


def getCost(infoCluster):
    return infoCluster[0] * infoCluster[1] * infoCluster[2] * (infoCluster[3] + infoCluster[4])


def costFuction(infoClusters):
    totalCost = 0
    for cluster in infoClusters:
        totalCost += getCost(cluster)
    return totalCost


def getWeightCluster(cluster, dataModel):
    weightOfPoints = dataModel.weightOfPoints
    weight = 0
    for point in cluster:
        weight += weightOfPoints[point]
    return weight

def getTotalWeight(clusters, dataModel):
    weight = []
    for cluster in clusters:
        weight.append(getWeightCluster(cluster, dataModel))
    return weight

def getQuantityOfPoint(solutionList):
    count = 0
    for cluster in solutionList:
        for _ in cluster:
            count += 1
    return count


def positionOfPoint(solutionList):
    quantityOfPoint = getQuantityOfPoint(solutionList)
    listPositionOfPoints = np.zeros(quantityOfPoint, dtype=int)
    for idxCluster in range(len(solutionList)):
        for point in solutionList[idxCluster]:
            listPositionOfPoints[point] = idxCluster
    return listPositionOfPoints


class Solution(State):
    """
    Contains a list of customers, weight list and distance matrix 
    """
    # costFuction = weightCluster*weightOfVehicle*maxRadiusCluster
    # *(MST + distanceToDepot + depotToMaxPointInCLuster + cardinalityOfCluster)
    # Index in infoClusters:
    # weightCluster: 0, weightOfVehicle: 1, radius: 2, MST: 3, distanceToDepot: 4

    def __init__(self, solutionArr: np.ndarray) -> None:
        self.solutionArr = solutionArr
        self.positionOfPoint = None
        self.infoClusters = None
        self.costFuction = None

    def getInfoClusters(self, dataModel: object, 
                        weightClusterSolution: np.ndarray, 
                        distanceMatrix: np.ndarray) -> list:
        return [getInfo(self.solutionArr[idxCluster],
                        weightClusterSolution[idxCluster],
                        dataModel.weightOfVehicle[idxCluster],
                        distanceMatrix,
                        dataModel.depot)
                for idxCluster in range(len(self.solutionArr))]

    def updatePositionOfPoint(self) -> None:
        self.positionOfPoint = positionOfPoint(self.solutionArr)

    def updateInfoClusters(self, dataModel, 
                           weightClusterSolution, distanceMatrix) -> None:
        self.infoClusters = self.getInfoClusters(
            dataModel, weightClusterSolution, distanceMatrix)

    def updateCostFuction(self) -> None:
        self.costFuction = costFuction(self.infoClusters)

    def updateSolution(self, dataModel, 
                       weightClusterSolution, 
                       distanceMatrix) -> None:
        self.updateInfoClusters(
            dataModel, weightClusterSolution, distanceMatrix)
        self.updateCostFuction()
        self.updatePositionOfPoint()

    def objective(self) -> int:
        return self.costFuction

    def __copy__(self) -> object:
        return self.__class__(deepcopy(self.solutionArr))


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

def getRadius(clusterList, distanceMatrix) -> float:
    radiusList = []
    for cluster in clusterList:
        radiusList.append(findMax(cluster, distanceMatrix))
    return radiusList
