import random
import numpy as np
import time
import numpy.random as rnd

from utils.data import readDistanceMatrix
from utils.solution import Solution, getTotalWeight
from Greedy import greedy
from utils.DataModel import DataModel
from writeGraph import draw ,drawInteractive
from Tabu import LocalSearch, checkConstraintSatisfiedSolution, Tabu


from operatorAlns import *
from alns import ALNS, State
from alns.accept import HillClimbing
from alns.select import RouletteWheel
from alns.stop import MaxRuntime

random.seed(3)
np.random.seed(3)

# create a matrix
x = np.random.randint(0, 200, 121)
y = np.random.randint(0, 200, 121)
z = np.array([complex(x[i], y[i]) for i in range(x.size)])
m, n = np.meshgrid(z, z)
distanceMatrix = abs(m-n)


quantityOfPoint = 121
p = 10
weightCluster = [30, 30, 30, 30, 20, 20, 20, 40, 40, 40]
depot = 121
# minWeight = 1
# maxWeight = 3
# weightOfPoints = [random.randint(minWeight, maxWeight) for i in range(len(distanceMatrix))]
SEED = 1
rndState = np.random.RandomState(SEED)
weightOfPoints = [1, 3, 1, 2, 1, 2, 2, 2, 3, 2, 1, 1, 2, 1, 2, 2, 3, 1, 3, 2, 2, 3, 1, 3, 1, 2, 1, 1, 1, 3, 3, 1, 2, 3, 1, 2, 3, 1, 3, 1, 2, 2, 3, 1, 2, 1, 3, 1, 2, 2, 1, 2, 3, 3, 1, 1, 3, 3, 2, 1, 3, 2, 3, 3, 3, 2, 3, 3, 1, 2, 2, 3, 2, 3, 2, 3, 1, 2, 1, 3, 2, 2, 3, 1, 2, 3, 3, 3, 3, 2, 1, 2, 3, 3, 1, 1, 3, 2, 2, 2, 3, 1, 2, 1, 2, 3, 3, 3, 3, 2, 3, 1, 1, 3, 1, 1, 1, 3, 3, 1]
weightOfVehicle = random.choices([3, 5, 7], k=10)
dataModel = DataModel(quantityOfPoint, weightCluster, 
                      weightOfPoints, weightOfVehicle, 
                      depot)



initSol = greedy(None, dataModel, distanceMatrix, rndState)
worstRemovalMST(initSol, rndState, distanceMatrix)
print(initSol.solutionArr)
greedy(initSol, dataModel, distanceMatrix, rndState)
# random_state = rnd.RandomState(SEED)
# alns = ALNS(random_state)

# alns.add_destroy_operator(worstRemovalMST)

# alns.add_repair_operator(greedy)


# select = RouletteWheel([25, 5, 1, 0], 0.8, 1, 1)
# accept = HillClimbing()
# stop = MaxRuntime(10)

# result = alns.iterate(initSol, select, accept, stop)

























# a = greedy(dataModel, distanceMatrix, rndState)
# # draw(x, y, a, depot) 
# b = localSearch(a, dataModel, distanceMatrix, rndState)
# print("----")
# weight = getTotalWeight(b.solutionList, dataModel)
# print(b.costFuction)
# b.updateSolution(dataModel, weight, distanceMatrix)
# print(b.costFuction)
# # print(f"test: {a.infoClusters}")
# # print(w)
# b = checkConstraintSatisfiedSolution(a.solutionList, 
#                                  dataModel.weightOfPoints, 
#                                  dataModel.weightCluster)
# print(b)
# # print(b.costFuction)
# # print(checkConstraintSatisfiedSolution(b.solutionList, 
# #                                  dataModel.weightOfPoints, 
# #                                  dataModel.weightCluster))
# # b.updateSolution(dataModel, getTotalWeight(b.solutionList, dataModel), distanceMatrix)
# # print(b.costFuction)
# draw(x, y, a, depot) 






