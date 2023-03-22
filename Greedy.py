import random
from writeGraph import draw

from utils.solution import *


def calculateRadius(point, clusterList, distanceMatrix):
    return max(clusterList, key=lambda secondPoint: distanceMatrix[
        point, secondPoint])

def findNextPoint(candidatePoints, weightOfPoints, weightCluster,
                  clustersList, currentWeight, 
                  distanceMatrix, weightOfVehicle, storeHouse):
    minDistance = float('inf')
    nextPoint = None
    nextCluster = None
    for point in candidatePoints:
        for idxCluster in range(len(clustersList)):
            cluster = clustersList[idxCluster]
            cost = 0
            if currentWeight[idxCluster] + weightOfPoints[point] <= weightCluster[idxCluster]:
                tempCluster = cluster + [point]
                radius = getMaxRadius(tempCluster, distanceMatrix)
                mstCluster = MST(tempCluster, distanceMatrix)[0]
                disToStorehouse = minDisPointToCluster(storeHouse - 1, tempCluster, distanceMatrix)
                cost = radius * weightOfVehicle[idxCluster] * (mstCluster + disToStorehouse)
                cost *= (currentWeight[idxCluster] + weightOfPoints[point])
                if cost < minDistance:
                    nextPoint = point
                    minDistance = cost
                    nextCluster = idxCluster

    return nextPoint, nextCluster


def addFirstPointInClusters(clustersList, candidatePoints, numberOfCluster, distanceMatrix):
    firstPointList = []
    firstPoint = random.choice(candidatePoints)
    candidatePoints.remove(firstPoint)
    clustersList[0].append(firstPoint)
    firstPointList.append(firstPoint)
    for idxcluster in range(1, numberOfCluster):
        nextPoint = findNextFirstPoint(firstPointList, candidatePoints, distanceMatrix)
        firstPointList.append(nextPoint)
        clustersList[idxcluster].append(nextPoint)
        candidatePoints.remove(nextPoint)


def findNextFirstPoint(firstPointList, candidatePoints, distanceMatrix):
    nextPoint = max(candidatePoints, key=lambda point: estimatedTotalDistance(
        point, firstPointList, distanceMatrix))
    return nextPoint


def estimatedTotalDistance(point, firstPointList, distanceMatrix):
    minDis = float('inf')
    if point not in firstPointList:
        for firstPoint in firstPointList:
            distance = distanceMatrix[point, firstPoint]
            if minDis > distance:
                minDis = distance
    return minDis    


def greedy(distanceMatrix, dataModel, verbose, x, y, clustersList=None):
    clustersList = []
    currentWeight = []

    weightCluster = dataModel.weightCluster
    weightOfPoints = dataModel.weightOfPoints
    weightOfVehicle = dataModel.weightOfVehicle
    numberOfPoint = len(distanceMatrix) - 1
    storeHouse = len(distanceMatrix)
    numberOfCluster = len(weightCluster)
 
    # if clustersList is not None:
    #     if 
    # else:
    #     for _ in range(numberOfCluster):
    #         clustersList.append([])
    #         currentWeight.append(0)

    #     candidatePoints = [point for point in range(numberOfPoint)]
    #     addFirstPointInClusters(clustersList, candidatePoints, numberOfCluster, distanceMatrix)
    #     # draw(x, y, clustersList)
    #     for idxCluster in range(numberOfCluster):
    #         for point in clustersList[idxCluster]:
    #             currentWeight[idxCluster] += weightOfPoints[point]
                
    while candidatePoints:
        nextPoint, nextCluster = findNextPoint(
            candidatePoints, weightOfPoints, weightCluster ,
            clustersList, currentWeight, distanceMatrix, 
            weightOfVehicle, storeHouse)
        candidatePoints.remove(nextPoint)
        clustersList[nextCluster].append(nextPoint)
        currentWeight[nextCluster] += weightOfPoints[nextPoint]

    return Solution(clustersList, currentWeight, distanceMatrix, dataModel)
