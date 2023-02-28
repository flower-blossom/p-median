from utils.data import readDistanceMatrix
from utils.solution import Solution, getRadius, findRadiusPoint
from Greedy import Greedy
from utils.DataModel import DataModel
from writeGraph import draw ,drawInteractive
from Tabu import LocalSearch, checkConstraintSatisfiedSolution, Tabu
import random
import numpy as np
random.seed(3)

np.random.seed(3)
x = np.random.randint(0, 200, 120)
y = np.random.randint(0, 200, 120)
z = np.array([complex(x[i], y[i]) for i in range(x.size)])
# print(z)
m, n = np.meshgrid(z, z)
# get the distance via the norm
distanceMatrix = abs(m-n)
# print(out)
# distanceMatrix = readDistanceMatrix("gr120", "distanceMatrices")

p = 10
weightCluster = [30, 30, 30, 30, 20, 20, 20, 40, 40, 40]

minWeight = 1
maxWeight = 3
# weightOfPoints = [random.randint(minWeight, maxWeight) for i in range(len(distanceMatrix))]
weightOfPoints = [1, 3, 1, 2, 1, 2, 2, 2, 3, 2, 1, 1, 2, 1, 2, 2, 3, 1, 3, 2, 2, 3, 1, 3, 1, 2, 1, 1, 1, 3, 3, 1, 2, 3, 1, 2, 3, 1, 3, 1, 2, 2, 3, 1, 2, 1, 3, 1, 2, 2, 1, 2, 3, 3, 1, 1, 3, 3, 2, 1, 3, 2, 3, 3, 3, 2, 3, 3, 1, 2, 2, 3, 2, 3, 2, 3, 1, 2, 1, 3, 2, 2, 3, 1, 2, 3, 3, 3, 3, 2, 1, 2, 3, 3, 1, 1, 3, 2, 2, 2, 3, 1, 2, 1, 2, 3, 3, 3, 3, 2, 3, 1, 1, 3, 1, 1, 1, 3, 3, 1]
weightOfVehicle = random.choices([3, 5, 7], k=10)

dataModel = DataModel(weightCluster, weightOfPoints, weightOfVehicle)



solution, currentSol = Tabu(dataModel, distanceMatrix, timeLimit=10, neighborSize=6, tabusSize=0.4,verbose=1).solve()
c = LocalSearch(dataModel, distanceMatrix, 1).solve(solution.__copy__())
# draw(x, y, solution.solutionList)
drawInteractive(x, y, c.solutionList, distanceMatrix)
# print(dataModel.weightCluster)
# b = LocalSearch(dataModel, distanceMatrix, 1).solve(solution_1)
# print(c.solutionList)
tabuSol = getRadius(solution.solutionList, distanceMatrix)
# currentSol = getRadius(currentSol.solutionList, distanceMatrix)
# draw(c.solutionList)
# locaTabuSol = getRadius(c.solutionList, distanceMatrix)

# localSol = getRadius(c.solutionList, distanceMatrix)
print(checkConstraintSatisfiedSolution(c.solutionList, weightOfPoints, weightCluster))
print(f"TabuSolution - {c.totalDistance}")
# print(f"tabuSol - {sum(tabuSol)}")
# print(f"tabuSol - {sum(currentSol)}")

# print(f"LocalSolution - {b.totalDistance}")
# print(f"tabuSol - {sum(localSol)}")
# print(f"Tabu+LocalSolution - {c.totalDistance}")
# print(f"locaTabuSol - {sum(locaTabuSol)}")
# print(checkConstraintSatisfiedSolution(solution.solutionList, weightOfPoints, weightCluster))

# 2368


