from copy import copy, deepcopy
from solution import Solution, getTotalDistance
import numpy as np
import random

class Scatter:
    def __init__(self, verbose=0):
        self.bestSolution = 0
        self.popSize = 10
        self.verbose = verbose

    def findFarthestCity(self, distanceMatrix, representList):
        max = float('-inf')
        maxTotalDistance = 0
        nextRepresent = -1
        for city in range(len(distanceMatrix)):
            maxTotalDistance = 0
            if city not in representList:
                for represent in representList:
                    distance = distanceMatrix[city, represent]
                    maxTotalDistance += distance
            if max < maxTotalDistance:
                    max = maxTotalDistance
                    nextRepresent = city    
        return nextRepresent
        
    def createSolution(self, distanceMatrix, partCityList, cityList, p):
        solutionList = []
        firstRepresent = random.choice(partCityList)
        partCityList.remove(firstRepresent)
        solutionList.append(firstRepresent)
        while len(solutionList) < p:
            nextCity = self.findFarthestCity(distanceMatrix, solutionList)
            solutionList.append(nextCity)
        
        # remove duplicate city
        solutionList = solutionList + list(set(cityList) - set(solutionList))    
        return Solution(solutionList, distanceMatrix, p)
        
    def createPopulation(self, distanceMatrix, p, popSize):
        pop = []
        cityList = [city for city in range(len(distanceMatrix))]
        random.shuffle(cityList)
        partitionCityLists = np.array_split(cityList, 3)
        partitionCityLists = [arr.tolist() for arr in partitionCityLists]
        while len(pop) < popSize:
            for partCityList in partitionCityLists:
                solution = self.createSolution(distanceMatrix, partCityList, cityList, p)
                pop.append(self.localSearch(solution, distanceMatrix, p))
        return pop

    # def GenerateReferenceSet(self, ):
    #     return pass

    # def selectSubset():

    def localSearch(self, solution, distanceMatrix, p):
        currentSolution = solution.__copy__()
        while True:
            firstSolutionList = currentSolution.solutionList.copy()
            firstTotalDistance = getTotalDistance(
                firstSolutionList, distanceMatrix, p)
            tempList = firstSolutionList.copy()
            for indexPresent in range(p):
                for indexCity in range(p + 1, len(distanceMatrix)):
                    tempList[indexPresent], tempList[indexCity] = tempList[indexCity], tempList[indexPresent]
                    totalDistance = getTotalDistance(
                        tempList, distanceMatrix, p)
                    if self.verbose == 1:
                        print(f"{totalDistance}: {currentSolution.totalDistance}")
                    if totalDistance < currentSolution.totalDistance:
                        currentSolution.solutionList = tempList.copy()
                        currentSolution.totalDistance = totalDistance
                        # print(totalDistance)
            if firstTotalDistance == currentSolution.totalDistance:
                solution.solutionList = currentSolution.solutionList.copy()
                solution.totalDistance = currentSolution.totalDistance
                return solution

    # def combineSolutions():

    def solve(self, distanceMatrix, p):
        a = self.createPopulation(distanceMatrix, p, self. popSize)
        for i in a:
            print(i.totalDistance)
        print(a)

