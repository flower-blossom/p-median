import random
from writeGraph import draw

from utils.solution import Solution




def calculateDistance(point, clusterList, distanceMatrix):
    maxDistance = 0
    for secondPoint in clusterList:
        distance = distanceMatrix[point, secondPoint]
        if maxDistance < distance:
            maxDistance = distance
    return maxDistance


class Greedy:

    def __init__(self, dataModel, distanceMatrix, verbose):
        self.weightCluster = dataModel.weightCluster
        self.weightOfPoints = dataModel.weightOfPoints
        # self.size = len(dataModel.distanceMatrix)
        self.distanceMatrix = distanceMatrix
        self.verbose = verbose
        self.comment = 'Greedy'

    def findNextPoint(self, candidatePoints, clustersList, currentWeight):
        minDistance = float('inf')
        nextPoint = None
        nextCluster = None
        for point in candidatePoints:
            for idxCluster in range(len(clustersList)):
                if currentWeight[idxCluster] + self.weightOfPoints[point] <= self.weightCluster[idxCluster]:
                    radius = calculateDistance(
                        point, clustersList[idxCluster], self.distanceMatrix)
                    if radius < minDistance:
                        nextPoint = point
                        minDistance = radius
                        nextCluster = idxCluster

        return nextPoint, nextCluster
    

    def addFirstPointInClusters(self, clustersList, candidatePoints, numberOfCluster):
        firstPointList = []
        firstPoint = random.choice(candidatePoints)
        candidatePoints.remove(firstPoint)
        clustersList[0].append(firstPoint)
        firstPointList.append(firstPoint)
        for Idxcluster in range(1, numberOfCluster):
            nextPoint = self.findNextFirstPoint(firstPointList, candidatePoints)
            firstPointList.append(nextPoint)
            clustersList[Idxcluster].append(nextPoint)
            candidatePoints.remove(nextPoint)


    def findNextFirstPoint(self, firstPointList, candidatePoints):
        nextPoint = sorted(candidatePoints, key=lambda point: self.estimatedTotalDistance(
            point, firstPointList), reverse=True)
        return nextPoint[0]      

    def estimatedTotalDistance(self, point, firstPointList):
        min = float('inf')
        if point not in firstPointList:
            for firstPoint in firstPointList:
                distance = self.distanceMatrix[point, firstPoint]
                if min > distance:
                    min = distance
        return min    

    def solve(self):
        # Print the header if verbose = 1 or verbose = 2
        if self.verbose == 1 or self.verbose == 2:
            print(self.comment)

        clustersList = []
        currentWeight = []
        numberOfPoint = len(self.distanceMatrix)
        numberOfCluster = len(self.weightCluster)

        for _ in range(numberOfCluster):
            clustersList.append([])
            currentWeight.append(0)
        candidatePoints = [point for point in range(numberOfPoint)]

        self.addFirstPointInClusters(clustersList, candidatePoints, numberOfCluster)
        for idxCluster in range(numberOfCluster):
            for point in clustersList[idxCluster]:
                currentWeight[idxCluster] += self.weightOfPoints[point]

        while candidatePoints:
            nextPoint, nextCluster = self.findNextPoint(
                candidatePoints, clustersList, currentWeight)
            candidatePoints.remove(nextPoint)
            clustersList[nextCluster].append(nextPoint)
            currentWeight[nextCluster] += self.weightOfPoints[nextPoint]

        solution = Solution(clustersList, currentWeight, self.distanceMatrix)

        # Print the final result if verbose = 1 or verbose = 2
        if self.verbose == 1 or self.verbose == 2:
            print(f'Total Distance: {solution.totalDistance}\n')
        return solution
