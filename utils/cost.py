import numpy as np
from pathlib import Path


def readDistanceMatrix(problemName, distanceMatricesFolder):
    """
    Read distance matrix from a txt file
    """
    distanceMatricesFolder = Path(distanceMatricesFolder)
    fileName = f'{problemName}.matrix.tsp'

    # Navigate to distanceMatrices file
    distanceMatrixPath = distanceMatricesFolder / fileName

    distanceMatrix = np.loadtxt(distanceMatrixPath, dtype=int)
    return distanceMatrix

# example: distanceMatricesFolder = "D:\Học\Thiết kế và đánh giá thuật toán\p-median\distanceMatrices"


distanceMatricesFolder = r"C:\Users\Lenovo\Downloads\matrix_distance"

problemName = "ulysses16"
A = readDistanceMatrix(problemName, distanceMatricesFolder)


class Solution:
    """
    Contains a list of customers and distanceMatrix
    """

    def __init__(self, solutionMatrix, distanceMatrix):
        self.solutionMatrix = solutionMatrix
        self.distanceMatrix = distanceMatrix
        self.totalDistance = self.__getTotalDistance()

    def __getTotalDistance(self):

        distance = 0

        remain = np.arange(len(self.distanceMatrix))  # remain là các thành phố
        # lọc các nhiệm ra khỏi các thành phố
        remain = np.setdiff1d(np.array(remain), np.array(self.solutionMatrix))

        max_ = np.amax(self.distanceMatrix) + 1
        min_ = max_

        for i in remain:
            for j in self.solutionMatrix:

                if(A[i, j] < min_ and i != j):
                    # location = j
                    min_ = self.distanceMatrix[i, j]
            distance = distance + min_
            min_ = max_
        return distance


s1 = Solution([1, 2, 3], A)

print(s1.totalDistance)
