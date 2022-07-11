from copy import copy, deepcopy
from solution import Solution, getTotalDistance
from itertools import combinations
import time 
import numpy as np
import random


class Scatter:
    def __init__(self, popSize=10, refSetSize=5, subSetSize=2,verbose=0, alpha=0.3, beta=0.3, gamma=0.2, timeLimit=300):
        self.refSetSize = refSetSize
        self.subSetSize = subSetSize
        self.popSize = popSize
        self.verbose = verbose
        self.gamma = gamma
        self.alpha = alpha
        self.beta = beta
        self.timeLimit = timeLimit
        self.bestSoluiton = None
        self.timeStart = None

    def estimatedTotalDistance(self, city, distanceMatrix, representList):
        distance = 0
        if city not in representList:
            for represent in representList:
                distance += distanceMatrix[city, represent]
        return distance


    def candidateList(self, distanceMatrix, representList, maxTotalDistance):
        candidateList = []
        for city in range(len(distanceMatrix)):
            distance = self.estimatedTotalDistance(city, distanceMatrix, representList)
            if maxTotalDistance*(1 - self.gamma) < distance:
                candidateList.append(city)
        return candidateList

    def findNextCity(self, distanceMatrix, representList):
        citys = [city for city in range(len(distanceMatrix))]
        maxTotalDistance = max(citys, key=lambda city: self.estimatedTotalDistance(city, distanceMatrix, representList))
        candidateList = self.candidateList(distanceMatrix, representList, maxTotalDistance)
        return random.choice(candidateList)

    def createSolution(self, distanceMatrix, partCityList, cityList, p):
        solutionList = []
        firstRepresent = random.choice(partCityList)
        solutionList.append(firstRepresent)
        while len(solutionList) < p:
            nextCity = self.findNextCity(distanceMatrix, solutionList)
            solutionList.append(nextCity)

        # remove duplicate city
        solutionList = solutionList + list(set(cityList) - set(solutionList))
        return Solution(solutionList, distanceMatrix, p)

    def scoringForSolution(self, solution, pop):
        minScoreSolution = min(pop, key=lambda solutionInPop: solutionInPop.totalDistance + solution.totalDistance)
        score = solution.totalDistance - self.beta * (minScoreSolution.totalDistance + solution.totalDistance)
        return score

    def addGoodSolution(self, pop, distanceMatrix, p, partitionCityLists, cityList):
        while len(pop) < self.alpha*self.popSize:
            for partCityList in partitionCityLists:
                solution = self.createSolution(
                    distanceMatrix, partCityList, cityList, p)
                solution = self.localSearch(solution, distanceMatrix, p)
                condition = True
                for sol in pop:
                    if sol.totalDistance == solution.totalDistance:
                        condition = False
                if condition:
                    pop.append(solution)  

    def addDisperseSolutions(self, pop, distanceMatrix, p, partitionCityLists, cityList):
        while len(pop) < self.popSize:
            createSolution = [self.createSolution(
                    distanceMatrix, partCityList, cityList, p) for partCityList in partitionCityLists]
            solution = max(createSolution, key=lambda solution: self.scoringForSolution(solution, pop))  
            condition = True      
            for sol in pop:
                if sol.totalDistance == solution.totalDistance:
                    condition = False
            if condition:
                pop.append(solution)  

    def createPopulation(self, distanceMatrix, p):
        pop = []
        cityList = [city for city in range(len(distanceMatrix))]
        random.shuffle(cityList)
        partitionCityLists = np.array_split(cityList, p/4)
        partitionCityLists = [arr.tolist() for arr in partitionCityLists]
        self.addGoodSolution(pop, distanceMatrix, p, partitionCityLists, cityList)
        self.addDisperseSolutions(pop, distanceMatrix, p, partitionCityLists, cityList)
        return pop

    def generateReferenceSet(self, pop):
        refSetSize = []
        sortedPop = sorted(pop, key=lambda solution: solution.totalDistance)
        for idx in range(round(self.refSetSize/2)):
            refSetSize.append(sortedPop[idx])
        while len(refSetSize) < self.refSetSize:
            refSetSize.append(sortedPop[-1])
            sortedPop.pop()
        self.bestSoluiton = refSetSize[0].__copy__()
        return refSetSize

    def selectSubset(self, refSetSize):
        subSets = combinations(refSetSize, self.subSetSize)
        return subSets

    def combineSolutions(self, subSet):
        solution1 = subSet[0]
        solution2 = subSet[1]



    def localSearch(self, solution, distanceMatrix, p):
        currentSolution = solution.__copy__()
        cityQuantity = len(distanceMatrix)
        while True:
            firstSolutionList = currentSolution.solutionList.copy()
            firstTotalDistance = getTotalDistance(
                firstSolutionList, distanceMatrix, p)
            tempList = firstSolutionList.copy()
            for indexPresent in range(p):
                for indexCity in range(p, cityQuantity):
                    tempList[indexPresent], tempList[indexCity] = tempList[indexCity], tempList[indexPresent]
                    totalDistance = getTotalDistance(tempList, distanceMatrix, p)
                    if self.verbose == 1:
                        print(f"{totalDistance}: {currentSolution.totalDistance}")
                    if totalDistance < currentSolution.totalDistance:
                        currentSolution.solutionList = tempList.copy()
                        currentSolution.totalDistance = totalDistance
                        if self.bestSoluiton is not None:
                            if currentSolution.totalDistance < self.bestSoluiton.totalDistance:
                                self.bestSoluiton = currentSolution.__copy__()
                        else:
                            self.bestSoluiton = currentSolution.__copy__()
                    else:                        
                        tempList[indexPresent], tempList[indexCity] = tempList[indexCity], tempList[indexPresent]    
                    if time.time() - self.timeStart > self.timeLimit:
                        if currentSolution.totalDistance < self.bestSoluiton.totalDistance:
                            self.bestSoluiton = currentSolution.__copy__()
                        break    
                        # return self.bestSoluiton

            if firstTotalDistance == currentSolution.totalDistance:
                solution.solutionList = firstSolutionList
                solution.totalDistance = firstTotalDistance
                if self.bestSoluiton is not None:
                    if solution.totalDistance < self.bestSoluiton.totalDistance:
                        self.bestSoluiton = solution.__copy__()
                else:
                    self.bestSoluiton = solution.__copy__()
                return solution


    def solve(self, distanceMatrix, p):
        self.timeStart = time.time()
        while True:
            pop = self.createPopulation(distanceMatrix, p)
            # while time.time() - self.timeStart > self.timeLimit:
            #     refSetSize = self.generateReferenceSet(pop)
                # subsets = self.selectSubset(refSetSize)
                # for subset in subsets:
                #     solution = self.combineSolutions(subset)
                #     self.localSearch(solution, distanceMatrix, p)
                    # if time.time() - self.timeStart > self.timeLimit:
                    #     return self.bestSoluiton
                # if time.time() - self.timeStart > self.timeLimit:
                #     return self.bestSoluiton
            if time.time() - self.timeStart > self.timeLimit:
                return self.bestSoluiton
        return self.bestSoluiton
