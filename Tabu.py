from numpy import zeros
from random import sample, choice
import time

from Greedy import greedy, calculateRadius
from utils.solution import findMax


def positionOfPoint(solutionList, quantityOfPoint):
    listPositionOfPoints = zeros(quantityOfPoint, dtype=int)
    for idxCluster in range(len(solutionList)):
        for point in solutionList[idxCluster]:
            listPositionOfPoints[point] = idxCluster
    return listPositionOfPoints

def checkConstraintSatisfiedSolution(solutionList, weightOfPoints, limitWeightCluster):
    checkWeight = []
    for idxCluster in range(len(solutionList)):
        sumWeight = 0                    
        for point in solutionList[idxCluster]:
            # print(f"point: {point} - { weightOfPoints[point]}")
            sumWeight += weightOfPoints[point]
        print(f"{sumWeight} - {limitWeightCluster[idxCluster]}")
        if sumWeight > limitWeightCluster[idxCluster]:
            # return False
            
            checkWeight.append(False)
        else:
            checkWeight.append(True)
    return checkWeight 

def isValidCondition(weightOfPoints, limitWeightCluster, weightClusterSolution, firstPoint, idxFirstCluster,
                     idxSecondCluster, secondPoint=None):
    weightFirstClusterAfter = 0
    weightSecondClusterAfter = 0
    if secondPoint is not None:
        weightFirstClusterAfter = weightClusterSolution[idxFirstCluster] - \
            weightOfPoints[firstPoint] + weightOfPoints[secondPoint]
        weightSecondClusterAfter = weightClusterSolution[idxSecondCluster] - \
            weightOfPoints[secondPoint] + weightOfPoints[firstPoint]
        if (weightFirstClusterAfter <= limitWeightCluster[idxFirstCluster] and
                weightSecondClusterAfter <= limitWeightCluster[idxSecondCluster]):
            return True
    else:
        if (weightClusterSolution[idxSecondCluster] + weightOfPoints[firstPoint] <=
                limitWeightCluster[idxSecondCluster]):
            return True
    return False

def changeClusterWeightCurrent(weightOfPoints, weightClusterSolution, firstPoint, idxFirstCluster,
                     idxSecondCluster, secondPoint=None):
    if secondPoint is not None:
        weightClusterSolution[idxFirstCluster] -= weightOfPoints[firstPoint] 
        weightClusterSolution[idxFirstCluster] += weightOfPoints[secondPoint]
        weightClusterSolution[idxSecondCluster] -= weightOfPoints[secondPoint] 
        weightClusterSolution[idxSecondCluster] += weightOfPoints[firstPoint]
    else:
        weightClusterSolution[idxFirstCluster] -= weightOfPoints[firstPoint] 
        weightClusterSolution[idxSecondCluster] += weightOfPoints[firstPoint] 

def distanceVaries(distanceMatrix, firstPoint, firstCluster, radiusFirstCluster,
                   secondCluster, radiusSecondCluster, secondPoint=None):
    totalChange = 0
    newRadiusFirstCluster = 0
    newRadiusSecondCluster = 0
    idxFirstPoint = firstCluster.index(firstPoint)
    if secondPoint is not None:
        idxSecondPoint = secondCluster.index(secondPoint)
        firstCluster[idxFirstPoint], secondCluster[idxSecondPoint] = secondCluster[idxSecondPoint], firstCluster[idxFirstPoint]
        newRadiusFirstCluster = findMax(firstCluster, distanceMatrix)
        newRadiusSecondCluster = findMax(
            secondCluster, distanceMatrix)
        firstCluster[idxFirstPoint], secondCluster[idxSecondPoint] = secondCluster[idxSecondPoint], firstCluster[idxFirstPoint]
    else:
        firstCluster.remove(firstPoint)
        newRadiusFirstCluster = findMax(firstCluster, distanceMatrix)
        estimatePointDistance = calculateRadius(
            firstPoint, secondCluster, distanceMatrix)
        secondCluster.append(firstPoint)
        if estimatePointDistance > radiusSecondCluster:
            newRadiusSecondCluster = estimatePointDistance
        else:
            newRadiusSecondCluster = findMax(
                secondCluster, distanceMatrix)
        firstCluster.append(firstPoint)
        secondCluster.remove(firstPoint)

    totalChange += (radiusFirstCluster + radiusSecondCluster)
    totalChange -= (newRadiusFirstCluster + newRadiusSecondCluster)
    return totalChange, newRadiusFirstCluster, newRadiusSecondCluster


def swapPoint(firstPoint, firstCluster, secondCluster, secondPoint):
    idxFirstPoint = firstCluster.index(firstPoint)
    idxSecondPoint = secondCluster.index(secondPoint)
    firstCluster[idxFirstPoint], secondCluster[idxSecondPoint] = secondCluster[idxSecondPoint], firstCluster[idxFirstPoint]


def movePoint(point, firstCluster, secondCluster):
    firstCluster.remove(point)
    secondCluster.append(point)


class Tabu:
    classAbbreviation = 'tabu'

    def __init__(self, dataModel, distanceMatrix, verbose=1, timeLimit=None, neighborSize=3, tabusSize=0.3):
        self.dataModel = dataModel
        self.limitWeightCluster = dataModel.weightCluster
        self.weightOfPoints = dataModel.weightOfPoints
        self.distanceMatrix = distanceMatrix
        self.__verbose = verbose
        self.__neighborSize = neighborSize
        self.__tabusSize = tabusSize
        self.bestSolution = None
        self.__timeLimit = timeLimit
        self.constraintSatisfiedState = None
        self.comment = f'Tabu - tabusSize: {tabusSize} - neighborSize: {neighborSize}'

    # def auxiliaryObjectives(self):

    def setConstraintSatisfiedState(self, weightClusterSolution, limitWeightCluster, clusterQuantity):
        
        for idxCluster in range(clusterQuantity):
            if weightClusterSolution[idxCluster] > limitWeightCluster[idxCluster]:
                self.constraintSatisfiedState = False
                return None
        self.constraintSatisfiedState = True


    def __initialSolution(self):
        """
        Create initial solution by Greedy if first solution is None.
        """
        solution = greedy(self.dataModel, self.distanceMatrix, 1).solve()
        self.bestSolution = solution.__copy__()
        return solution

    def ____createMovePointNeighbor(self, quantityCustomer, quantityCluster):
        spaceOfClusters = range(quantityCluster)
        spaceOfPoints = range(quantityCustomer)
        numberOfNeighbor = int(1/2*quantityCustomer * self.__neighborSize)
        neighborLists = [[choice(spaceOfPoints), choice(spaceOfClusters), 0]
                         for _ in range(numberOfNeighbor)]
        return neighborLists

    def ____createSwapPointNeighbor(self, quantityCustomer):
        spaceOfPoints = range(quantityCustomer)
        numberOfNeighbor = int(1/2*quantityCustomer * self.__neighborSize)
        return [sample(spaceOfPoints, k=2) + [1]
                for _ in range(numberOfNeighbor)]

    def __createNeighborList(self, quantityCustomer, quantityCluster):
        """
        Elements of neighbor is pair of customer index .
        """
        movePoint = self.____createMovePointNeighbor(
            quantityCustomer, quantityCluster)
        swapPoint = self.____createSwapPointNeighbor(quantityCustomer)
        return movePoint + swapPoint

    def __updateBestSolution(self, solution):
        """
        The best solution corresponds to the current solution.
        """
        self.bestSolution = solution.__copy__()

    def __checkTabus(self, neighbor, tabus):
        """
        Check the change is tabu or not by customer index is in tabus or not.
        """
        if neighbor[2] == 0:
            # Move point to new cluster
            return neighbor[0] in tabus
        else:     
            return neighbor[0] in tabus and neighbor[1] in tabus

    def __updateTabus(self, tabus, neighbor, quantityCustomer):
        """
        Update Tabus by add customer index changed in current solution
        """
        if neighbor[2] == 0:
            if neighbor[0] not in tabus:
                point = neighbor[0]
            else:
                return None
        else:     
            if neighbor[0] not in tabus:
                point = neighbor[0]
            elif neighbor[1] not in tabus:
                point = neighbor[1]
            else:
                return None
        if len(tabus) == round(quantityCustomer * self.__tabusSize):
            tabus.pop(0)
            tabus.append(point)
        else:
            tabus.append(point)

    # def __updateMatrix(self, diversificationMatrix, indexNeighborChange, solution):
    #     """
    #     Update matrix every time two customers swap places
    #     """
    #     customer1 = solution.customerList[indexNeighborChange[0]]
    #     customer2 = solution.customerList[indexNeighborChange[1]]
    #     diversificationMatrix[customer1, customer2] += 1
    #     diversificationMatrix[customer2, customer1] += 1
    #     return None

    def __allocateTimeForSections(self, customerQuantity):
        if customerQuantity <= 100:
            allocateTime = 4/5
        elif customerQuantity <= 1000:
            allocateTime = 3/4
        else:
            allocateTime = 1/2
        return allocateTime

        
    def estimatedDistance(self, neighbor, solution, listPositionOfPoint):
        point = neighbor[0]
        if neighbor[2] == 0:
            # Move point to new cluster
            idxNewCluster = neighbor[1]
            idxCurrentCluster = listPositionOfPoint[point]
            firstCluster = solution.solutionList[idxCurrentCluster]
            secondCluster = solution.solutionList[idxNewCluster]
            radiusFirstCluster = solution.radiusClusters[idxCurrentCluster]
            radiusSecondCluster = solution.radiusClusters[idxNewCluster]
            return distanceVaries(self.distanceMatrix, point, firstCluster, radiusFirstCluster,
                   secondCluster, radiusSecondCluster)
        else:     
            secondPoint = neighbor[1]
            idxFirstCluster = listPositionOfPoint[point]
            idxSecondCluster = listPositionOfPoint[secondPoint]
            # if idxFirstCluster == idxSecondCluster:
            #     return distanceVaries(self.distanceMatrix, point, firstCluster, radiusFirstCluster,
            #        secondCluster, radiusSecondCluster)
            # else:
            firstCluster = solution.solutionList[idxFirstCluster]
            secondCluster = solution.solutionList[idxSecondCluster]
            radiusFirstCluster = solution.radiusClusters[idxFirstCluster]
            radiusSecondCluster = solution.radiusClusters[idxSecondCluster]                 
            return distanceVaries(self.distanceMatrix, point, firstCluster, radiusFirstCluster,
                secondCluster, radiusSecondCluster, secondPoint)
        
    def isValidNeighbor(self, neighbor, solution, listPositionOfPoint):
        point = neighbor[0]
        weightClusterSolution = solution.weightClusterSolution
        weightOfPoints = self.weightOfPoints
        if neighbor[2] == 0:
            # Move point to new cluster
            idxNewCluster = neighbor[1]
            idxCurrentCluster = listPositionOfPoint[point]
            if idxNewCluster == idxCurrentCluster:
                return False
            return isValidCondition(weightOfPoints, self.limitWeightCluster, weightClusterSolution, 
                                    point, idxCurrentCluster,
                                    idxNewCluster)
            # return self.weightValidCondition(weightOfPoints, weightClusterSolution, 
            #                                  point, idxCurrentCluster,
            #                                 idxNewCluster)
        else:     
            secondPoint = neighbor[1]
            idxFirstCluster = listPositionOfPoint[point]
            idxSecondCluster = listPositionOfPoint[secondPoint]
            if idxFirstCluster == idxSecondCluster:
                return False
            return isValidCondition(weightOfPoints, self.limitWeightCluster, weightClusterSolution, 
                                    point, idxFirstCluster,
                                    idxSecondCluster, secondPoint=secondPoint)
            # return self.weightValidCondition(weightOfPoints, weightClusterSolution, 
            #                                  point, idxFirstCluster, idxSecondCluster,
            #                                  secondPoint)

    def weightValidCondition(self, weightOfPoints, weightClusterSolution, firstPoint, idxFirstCluster,
                     idxSecondCluster, secondPoint=None):
        weightCodition = 0
        weightFirstClusterAfter = 0
        weightSecondClusterAfter = 0
        currentWeightFirstCLuster = weightClusterSolution[idxFirstCluster]
        currentWeightSecondCLuster = weightClusterSolution[idxSecondCluster]
        maxWeightFirstCluster = self.limitWeightCluster[idxFirstCluster]
        maxWeightSecondCluster = self.limitWeightCluster[idxSecondCluster]
        if secondPoint is not None:
            weightFirstClusterAfter = weightClusterSolution[idxFirstCluster] - \
                weightOfPoints[firstPoint] + weightOfPoints[secondPoint]
            weightSecondClusterAfter = weightClusterSolution[idxSecondCluster] - \
                weightOfPoints[secondPoint] + weightOfPoints[firstPoint]
            
        else:
            weightFirstClusterAfter = weightClusterSolution[idxFirstCluster] - weightOfPoints[firstPoint]
            weightSecondClusterAfter = weightClusterSolution[idxSecondCluster] + weightOfPoints[firstPoint] 

        if (currentWeightFirstCLuster > maxWeightFirstCluster and 
            weightFirstClusterAfter <= maxWeightFirstCluster):
            weightCodition -= 1
        if (currentWeightSecondCLuster > maxWeightSecondCluster and 
            weightSecondClusterAfter <= maxWeightSecondCluster):
            weightCodition -= 1

        if (weightFirstClusterAfter <= maxWeightFirstCluster and
                weightSecondClusterAfter <= maxWeightSecondCluster):
            weightCodition += 0
        else: 
            if weightFirstClusterAfter > maxWeightFirstCluster:
                weightCodition += 1
            if weightSecondClusterAfter > maxWeightSecondCluster:
                weightCodition += 1

        return weightCodition    

    def compareToCurrentSol(self, distanceVariesChange):
        return distanceVariesChange > 0

    def compareToBestSol(self, solution):
        return solution.totalDistance < self.bestSolution.totalDistance

    def changeSolution(self, solution, neighbor, distanceVariesChange, listPositionOfPoint):
        solution.totalDistance -= distanceVariesChange[0]
        radiusClusters = solution.radiusClusters
        weightClusterSolution = solution.weightClusterSolution
        point = neighbor[0]
        solutionList = solution.solutionList
        if neighbor[2] == 0:
            # Move point to new cluster
            idxNewCluster = neighbor[1]
            idxCurrentCluster = listPositionOfPoint[point]
            movePoint(point, solutionList[idxCurrentCluster], solutionList[idxNewCluster])
            radiusClusters[idxCurrentCluster] = distanceVariesChange[1]
            radiusClusters[idxNewCluster] = distanceVariesChange[2]
            listPositionOfPoint[point] = idxNewCluster
            changeClusterWeightCurrent(self.weightOfPoints, weightClusterSolution, 
                                    point, idxCurrentCluster, idxNewCluster)
        else:     
            # Swap two point
            secondPoint = neighbor[1]
            idxFirstCluster = listPositionOfPoint[point]
            idxSecondCluster = listPositionOfPoint[secondPoint]
            radiusClusters[idxFirstCluster] = distanceVariesChange[1]
            radiusClusters[idxSecondCluster] = distanceVariesChange[2]
            listPositionOfPoint[point] = idxSecondCluster
            listPositionOfPoint[secondPoint] = idxFirstCluster
            swapPoint(point, solutionList[idxFirstCluster], solutionList[idxSecondCluster], secondPoint)
            changeClusterWeightCurrent(self.weightOfPoints, weightClusterSolution, 
                        point, idxFirstCluster, idxSecondCluster, secondPoint)

    def __mainTabu(self, currentSolution, listPositionOfPoint, pointQuantity, clusterQuantity, tabus):
        weightClusterSolution = currentSolution.weightClusterSolution

        self.setConstraintSatisfiedState(weightClusterSolution, self.limitWeightCluster, clusterQuantity)

        # neighborsList = sorted(neighborsList, key=lambda neighbor: (diversificationMatrix[neighbor[0], neighbor[1]],
        #                        - self.__distanceVariesTwoOpt(neighbor, currentSolution)), reverse=True)
        neighborsList = self.__createNeighborList(pointQuantity, clusterQuantity)

        neighborsList = sorted(neighborsList, key=lambda neighbor: 
                                   self.estimatedDistance(neighbor, currentSolution, listPositionOfPoint),
                                    reverse=True)
        # for i in neighborsList:
        #     print(f"{i} -{self.estimatedDistance(i, currentSolution, listPositionOfPoint)} - {self.isValidNeighbor(i, currentSolution, listPositionOfPoint)}")    
        neighbor = 0
        distanceVariesChange = 0

        while neighborsList:
            neighbor = neighborsList[0]
            neighborsList.pop(0)
            if self.isValidNeighbor(neighbor, currentSolution, listPositionOfPoint) is True:
                distanceVariesChange = self.estimatedDistance(neighbor, currentSolution, listPositionOfPoint)
                if self.compareToCurrentSol(distanceVariesChange[0]):
                    self.changeSolution(currentSolution, neighbor, distanceVariesChange, listPositionOfPoint)
                    if self.__verbose == 1 or self.__verbose == 2:
                        print(
                            f'Total Distance of current solution: {currentSolution.totalDistance}')
                    if self.compareToBestSol(currentSolution):
                        self.__updateBestSolution(currentSolution)
                        if self.__verbose == 1 or self.__verbose == 2:
                            print(
                                f'Total Distance of best solution: {self.bestSolution.totalDistance}')
                        self.__updateTabus(
                            tabus, neighbor, pointQuantity)
                        terminationCriteriaStatus = True
                        return terminationCriteriaStatus
                    else:
                        
                        self.__updateTabus(
                            tabus, neighbor, pointQuantity)
                        terminationCriteriaStatus = False
                        return terminationCriteriaStatus
                else:
                    if self.__checkTabus(neighbor, tabus) is False:

                        self.changeSolution(currentSolution, neighbor, distanceVariesChange, listPositionOfPoint)
                        print(f'Total Distance of current solution: {currentSolution.totalDistance}')
                        self.__updateTabus(
                            tabus, neighbor, pointQuantity)
                        terminationCriteriaStatus = False
                        return terminationCriteriaStatus
        self.changeSolution(currentSolution, neighbor, listPositionOfPoint, listPositionOfPoint)
        self.__updateTabus(tabus, neighbor, pointQuantity)
        terminationCriteriaStatus = False
        return terminationCriteriaStatus

    def solve(self):
        if self.__verbose == 1 or self.__verbose == 2:
            print(self.comment)

        timeStart = time.time()
        tabus = []

        pointQuantity = len(self.distanceMatrix)
        # diversificationMatrix = zeros((pointQuantity, pointQuantity))
        currentSolution = self.__initialSolution()
        clusterQuantity = len(currentSolution.solutionList)
        allocateTime = self.__allocateTimeForSections(pointQuantity)
        terminationCriteriaStatus = False
        # localSearchModel = LocalSearch(self.__dataModel, currentSolution)
        # currentSolution = localSearchModel.solve(timeStart, self.__timeLimit)
        # self.__updateBestSolution(currentSolution)

        listPositionOfPoint = positionOfPoint(currentSolution.solutionList, pointQuantity)
        # for i in range(1):
        #     terminationCriteriaStatus = self.__mainTabu(
        #         currentSolution, listPositionOfPoint, pointQuantity, clusterQuantity, tabus)
            
        while True:

            terminationCriteriaStatus = self.__mainTabu(
                currentSolution, listPositionOfPoint, pointQuantity, clusterQuantity, tabus)
            # print(tabus)
            if self.__verbose == 2:
                print(
                    f'Total Distance of current solution: {currentSolution.totalDistance}')
                print(
                    f'Total Distance of best solution: {self.__bestSolution.totalDistance}')
            timeCheck = time.time()
            if self.__timeLimit is not None:
                if timeCheck - timeStart > allocateTime * self.__timeLimit:
                    break

        if self.__verbose == 1 or self.__verbose == 2:
            print(
                f'Total Distance of best solution: {self.bestSolution.totalDistance}\n')

        return self.bestSolution, currentSolution


class LocalSearch:
    def __init__(self, dataModel, distanceMatrix, verbose):
        self.limitWeightCluster = dataModel.weightCluster
        self.weightOfPoints = dataModel.weightOfPoints
        self.distanceMatrix = distanceMatrix
        self.verbose = verbose

    def mainLocalSearch(self, solution):
        quantityOfPoint = len(self.distanceMatrix)
        terminationCriteriaStatus = False
        weightClusterSolution = solution.weightClusterSolution
        radiusClusters = solution.radiusClusters
        solutionList = solution.solutionList
        listPositionOfPoint = positionOfPoint(solutionList, quantityOfPoint)

        for point in range(quantityOfPoint):
            condition = True
            idxCurrentCluster = listPositionOfPoint[point]
            firstCluster = solutionList[idxCurrentCluster]
            radiusFirstCluster = radiusClusters[idxCurrentCluster]

            for idxAnotherCluster in range(len(solutionList)):
                # try to move point to another cluster
                if idxCurrentCluster != idxAnotherCluster:
                    if isValidCondition(self.weightOfPoints, self.limitWeightCluster,
                                        weightClusterSolution, point, idxCurrentCluster,
                                        idxAnotherCluster):
                        secondCluster = solutionList[idxAnotherCluster]
                        radiusSecondCluster = radiusClusters[idxAnotherCluster]
                        infoSwap = distanceVaries(self.distanceMatrix, point,
                                                  firstCluster, radiusFirstCluster, secondCluster,
                                                  radiusSecondCluster)
                        changeDistance, newRadiusFirstCluster, newRadiusSecondCluster = infoSwap
                        if changeDistance > 0:
                            terminationCriteriaStatus = True
                            solution.totalDistance -= changeDistance
                            print(f"totalDistance: {solution.totalDistance}")
                            radiusClusters[idxCurrentCluster] = newRadiusFirstCluster
                            radiusClusters[idxAnotherCluster] = newRadiusSecondCluster
                            movePoint(point, firstCluster, secondCluster)
                            listPositionOfPoint[point] = idxAnotherCluster
                            changeClusterWeightCurrent(self.weightOfPoints, weightClusterSolution, 
                                                       point, idxCurrentCluster, idxAnotherCluster)
                            condition = False
                            break


            # try to swap point to another point in other cluster
            if condition is True:
                for anotherPoint in range(point + 1, quantityOfPoint):
                    idxSecondCluster = listPositionOfPoint[anotherPoint]
                    if idxSecondCluster != idxCurrentCluster:
                        secondCluster = solutionList[idxSecondCluster]
                        radiusSecondCluster = radiusClusters[idxSecondCluster]
                        if isValidCondition(self.weightOfPoints, self.limitWeightCluster,
                                            weightClusterSolution, point, idxCurrentCluster,
                                            idxSecondCluster, anotherPoint):
                            infoSwap = distanceVaries(self.distanceMatrix, point,
                                                      firstCluster, radiusFirstCluster,
                                                      secondCluster, radiusSecondCluster,
                                                      anotherPoint)
                            changeDistance, newRadiusFirstCluster, newRadiusSecondCluster = infoSwap
                            if changeDistance > 0:
                                terminationCriteriaStatus = True
                                solution.totalDistance -= changeDistance
                                print(
                                    f"totalDistance: {solution.totalDistance}")
                                radiusClusters[idxCurrentCluster] = newRadiusFirstCluster
                                radiusClusters[idxSecondCluster] = newRadiusSecondCluster
                                swapPoint(point, firstCluster,
                                          secondCluster, anotherPoint)
                                listPositionOfPoint[point] = idxSecondCluster
                                listPositionOfPoint[anotherPoint] = idxCurrentCluster
                                changeClusterWeightCurrent(self.weightOfPoints, weightClusterSolution, 
                                                point, idxCurrentCluster, idxSecondCluster, anotherPoint)
                                break

        return terminationCriteriaStatus

    def solve(self, solution):
        terminationCriteriaStatus = True
        while terminationCriteriaStatus:
            terminationCriteriaStatus = False
            terminationCriteriaStatus = self.mainLocalSearch(solution)
            # if time.time() - timeStart > timeLimit:
            #     break

        return solution
