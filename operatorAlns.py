import copy
from utils.solution import *
from numpy import zeros
from random import sample, choice
from writeGraph import draw, drawInteractive
from Greedy import greedy, calculateRadius


DEGREE_OF_DESTRUCTION = 0.1


def checkConstraintSatisfiedSolution(solutionList, weightOfPoints, limitWeightCluster):
    checkWeight = []
    for idxCluster in range(len(solutionList)):
        sumWeight = 0
        for point in solutionList[idxCluster]:
            sumWeight += weightOfPoints[point]
        print(f"{sumWeight} - {limitWeightCluster[idxCluster]}")
        if sumWeight > limitWeightCluster[idxCluster]:
            # return False

            checkWeight.append(False)
        else:
            checkWeight.append(True)
    return checkWeight


def isValidCondition(weightOfPoints, limitWeightCluster, infoClusters, 
                     firstPoint, idxFirstCluster,idxSecondCluster, 
                     secondPoint=None):
    weightFirstClusterAfter = 0
    weightSecondClusterAfter = 0
    if secondPoint is not None:
        weightFirstClusterAfter = infoClusters[idxFirstCluster][0] - \
            weightOfPoints[firstPoint] + weightOfPoints[secondPoint]
        weightSecondClusterAfter = infoClusters[idxSecondCluster][0] - \
            weightOfPoints[secondPoint] + weightOfPoints[firstPoint]
        if (weightFirstClusterAfter <= limitWeightCluster[idxFirstCluster] and
                weightSecondClusterAfter <= limitWeightCluster[idxSecondCluster]):
            return True
    else:
        if (infoClusters[idxSecondCluster][0] + weightOfPoints[firstPoint] <=
                limitWeightCluster[idxSecondCluster]):
            return True
    return False

def changeInfoCluster(infoClusters, idxCluster, newInfo):
    infoClusters[idxCluster] = newInfo


def getCostCluster(cluster, infoCluster, distanceMatrix, dataModel):
    info = getInfo(cluster, getWeightCluster(cluster, dataModel), 
                   infoCluster[1], distanceMatrix, dataModel.depot)
    return getCost(info), info
    

def distanceVaries(distanceMatrix, firstPoint, firstCluster, infoFirstCluster,
                   secondCluster, infoSecondCluster, dataModel, secondPoint=None):
    totalChange = 0
    newCostFirstCluster = 0
    newCostSecondCluster = 0
    costFirstCluster = getCost(infoFirstCluster)
    costSecondCluster = getCost(infoSecondCluster)
    idxFirstPoint = firstCluster.index(firstPoint)
    if secondPoint is not None:
        # Swap 2 point
        idxSecondPoint = secondCluster.index(secondPoint)
        firstCluster[idxFirstPoint], secondCluster[idxSecondPoint] = secondCluster[idxSecondPoint], firstCluster[idxFirstPoint]
        
        newCostFirstCluster, newInfoFirstCluster = getCostCluster(firstCluster, infoFirstCluster, 
                                             distanceMatrix, dataModel)
        newCostSecondCluster, newInfoSecondCluster  = getCostCluster(secondCluster, infoSecondCluster, 
                                             distanceMatrix, dataModel)
        firstCluster[idxFirstPoint], secondCluster[idxSecondPoint] = secondCluster[idxSecondPoint], firstCluster[idxFirstPoint]
    else:
        # Move point to another cluster
        firstCluster.remove(firstPoint)
        newCostFirstCluster, newInfoFirstCluster = getCostCluster(firstCluster, infoFirstCluster, 
                                             distanceMatrix, dataModel)
        
        secondCluster.append(firstPoint)
        newCostSecondCluster, newInfoSecondCluster = getCostCluster(secondCluster, infoSecondCluster, 
                                             distanceMatrix, dataModel)
        firstCluster.append(firstPoint)
        secondCluster.remove(firstPoint)

    totalChange += (costFirstCluster + costSecondCluster)
    totalChange -= (newCostFirstCluster + newCostSecondCluster)
    return totalChange, newInfoFirstCluster, newInfoSecondCluster


def swapPoint(firstPoint, firstCluster, secondCluster, secondPoint):
    idxFirstPoint = firstCluster.index(firstPoint)
    idxSecondPoint = secondCluster.index(secondPoint)
    firstCluster[idxFirstPoint], secondCluster[idxSecondPoint] = secondCluster[idxSecondPoint], firstCluster[idxFirstPoint]


def movePoint(point, firstCluster, secondCluster):
    firstCluster.remove(point)
    secondCluster.append(point)


# Destroy operators


def pointsToRemove(quantityOfPoint):
    return int(quantityOfPoint * DEGREE_OF_DESTRUCTION)


def determinePointToRemove(edgeMSTOfCluster, edgeToRemove, rndState):
    firstPoint = edgeToRemove[0]
    secondPoint = edgeToRemove[1]
    scoreFirstPoint = 0
    scoreSecondPoint = 0
    for edge in edgeMSTOfCluster:
        pairOfPoint = [edge[0], edge[0]]
        if firstPoint in pairOfPoint:
            scoreFirstPoint += 1
        if secondPoint in pairOfPoint:
            scoreSecondPoint += 1
    if scoreFirstPoint > scoreSecondPoint:
        return secondPoint
    elif scoreFirstPoint < scoreSecondPoint:
        return firstPoint
    else:
        return rndState.choice([firstPoint, secondPoint])


def worstRemovalMST(current, rndState, distanceMatrix):
    """
    Worst removal iteratively removes the 'worst' edges, that is,
    those edges that have the largest distance.
    """
    destroyed = copy.deepcopy(current)
    solutionList = destroyed.solutionList
    indexClusters = destroyed.positionOfPoint
    quantityOfPoint = len(distanceMatrix) - 1

    edgeMST = []
    edgeMSTofSolution = []
    for cluster in destroyed.solutionList:
        temp = MST(cluster, distanceMatrix)[1]
        edgeMST.append(temp)
        edgeMSTofSolution += temp

    worstEdges = sorted(edgeMSTofSolution, key=lambda edge: edge[2], reverse=True)

    for idx in range(pointsToRemove(quantityOfPoint)):
        point = determinePointToRemove(edgeMST, worstEdges[idx], rndState)
        
        idxClusterOfPointToRemove = indexClusters[point]
        if idxClusterOfPointToRemove == -1:
            pass
        else:
            print(f"point: {point}")
            solutionList[idxClusterOfPointToRemove].remove(point)
            indexClusters[point] = -1
        

    return destroyed


# Repair operators

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
                disToStorehouse = minDisPointToCluster(
                    storeHouse - 1, tempCluster, distanceMatrix)
                cost = radius * \
                    weightOfVehicle[idxCluster] * \
                    (mstCluster + disToStorehouse)
                cost *= (currentWeight[idxCluster] + weightOfPoints[point])
                if cost < minDistance:
                    nextPoint = point
                    minDistance = cost
                    nextCluster = idxCluster

    return nextPoint, nextCluster


def addFirstPointInClusters(clustersList, candidatePoints,
                            numberOfCluster, distanceMatrix,
                            rndState):
    firstPointList = []
    firstPoint = rndState.choice(candidatePoints)
    candidatePoints.remove(firstPoint)
    clustersList[0].append(firstPoint)
    firstPointList.append(firstPoint)
    for idxcluster in range(1, numberOfCluster):
        nextPoint = findNextFirstPoint(
            firstPointList, candidatePoints, distanceMatrix)
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


def getUnvisitedPoint(solutionList, quantityOfPoint, depot):
    pointInList = []
    for cluster in solutionList:
        pointInList += cluster
    unvisitedPoint = [point for point in range(quantityOfPoint)
                      if point not in [depot]
                      if point not in pointInList]
    return unvisitedPoint
    # for cluster in solutionList:
    #     for point in cluster:
    #         unvisitedPoint.remove(point)


def greedy(solution, dataModel, distanceMatrix, rndState):
    depot = dataModel.depot
    quantityOfPoint = dataModel.quantityOfPoint
    weightCluster = dataModel.weightCluster
    weightOfPoints = dataModel.weightOfPoints
    weightOfVehicle = dataModel.weightOfVehicle
    numberOfPoint = len(distanceMatrix) - 1
    numberOfCluster = len(weightCluster)

    currentWeight = []
    if solution is None:
        clustersList = []
        for _ in range(numberOfCluster):
            clustersList.append([])

        candidatePoints = [point for point in range(numberOfPoint)]
        addFirstPointInClusters(clustersList, candidatePoints,
                                numberOfCluster, distanceMatrix,
                                rndState)
        for cluster in clustersList:
            currentWeight.append(getWeightCluster(cluster, dataModel))
    else:
        clustersList = solution.solutionList
        for cluster in clustersList:
            currentWeight.append(getWeightCluster(cluster, dataModel))
        candidatePoints = getUnvisitedPoint(
            clustersList, quantityOfPoint, depot)

    # draw(x, y, clustersList)
    while candidatePoints:
        nextPoint, nextCluster = findNextPoint(
            candidatePoints, weightOfPoints, weightCluster,
            clustersList, currentWeight, distanceMatrix,
            weightOfVehicle, depot)
        candidatePoints.remove(nextPoint)
        clustersList[nextCluster].append(nextPoint)
        currentWeight[nextCluster] += weightOfPoints[nextPoint]

    sol = Solution(clustersList)
    sol.updateSolution(dataModel, currentWeight, distanceMatrix)
    
    # localSearch(sol, dataModel, distanceMatrix, rndState)
    return sol



# Local search


def mainLocalSearch(solution, dataModel, distanceMatrix, rndState):
    limitWeightCluster = dataModel.weightCluster
    weightOfPoints = dataModel.weightOfPoints
    quantityOfPoint = dataModel.quantityOfPoint
    terminationCriteriaStatus = False
    infoClusters = solution.infoClusters
    solutionList = solution.solutionList
    listPositionOfPoint = solution.positionOfPoint

    for point in range(quantityOfPoint - 1):
        condition = True
        
        idxCurrentCluster = listPositionOfPoint[point]
        firstCluster = solutionList[idxCurrentCluster]
        infoFirstCluster = infoClusters[idxCurrentCluster]
                
        # try to move point to another cluster
        for idxAnotherCluster in range(len(solutionList)):
            if (idxCurrentCluster != idxAnotherCluster and
                isValidCondition(weightOfPoints, limitWeightCluster,
                                    infoClusters, point, idxCurrentCluster, 
                                    idxAnotherCluster)):

                    secondCluster = solutionList[idxAnotherCluster]
                    infoSecondCluster = infoClusters[idxAnotherCluster]
                    
                    infoSwap = distanceVaries(distanceMatrix, point, firstCluster, 
                                            infoFirstCluster, secondCluster,
                                            infoSecondCluster, dataModel)
                    changeDistance, newInfoFirstCluster, newInfoSecondCluster = infoSwap

                    if changeDistance > 0:
                        terminationCriteriaStatus = True
                        solution.costFuction -= changeDistance
                        print(f"totalDistance: {solution.costFuction}")
                        
                        movePoint(point, firstCluster, secondCluster)
                        changeInfoCluster(infoClusters, idxCurrentCluster, newInfoFirstCluster)
                        changeInfoCluster(infoClusters, idxAnotherCluster, newInfoSecondCluster)
                        listPositionOfPoint[point] = idxAnotherCluster
                        condition = False
                        break

        # try to swap point to another point in other cluster
        if condition is True:
            for anotherPoint in range(point + 1, quantityOfPoint - 1):
                idxSecondCluster = listPositionOfPoint[anotherPoint]
                if idxSecondCluster != idxCurrentCluster:
                    secondCluster = solutionList[idxSecondCluster]
                    infoSecondCluster = infoClusters[idxSecondCluster]
                    if isValidCondition(weightOfPoints, limitWeightCluster,
                                    infoClusters, point, idxCurrentCluster, 
                                    idxSecondCluster, anotherPoint):
                        infoSwap = distanceVaries(distanceMatrix, point, firstCluster, 
                                            infoFirstCluster, secondCluster,
                                            infoSecondCluster, dataModel,
                                            anotherPoint)                        
                        changeDistance, newInfoFirstCluster, newInfoSecondCluster = infoSwap
                        if changeDistance > 0:
                            terminationCriteriaStatus = True
                            solution.costFuction -= changeDistance
                            print(
                                f"totalDistance: {solution.costFuction}")
                            swapPoint(point, firstCluster,
                                        secondCluster, anotherPoint)
                            changeInfoCluster(infoClusters, idxCurrentCluster, newInfoFirstCluster)
                            changeInfoCluster(infoClusters, idxSecondCluster, newInfoSecondCluster)
                            listPositionOfPoint[point] = idxSecondCluster
                            listPositionOfPoint[anotherPoint] = idxCurrentCluster
                            break

    return terminationCriteriaStatus


def localSearch(solution, dataModel, distanceMatrix, rndState):
    terminationCriteriaStatus = True
    while terminationCriteriaStatus:
        terminationCriteriaStatus = False
        terminationCriteriaStatus = mainLocalSearch(
            solution, dataModel, distanceMatrix, rndState)
    return solution



# def splitPoint(point1):