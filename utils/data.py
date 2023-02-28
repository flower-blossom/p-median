from pathlib import Path
import numpy as np

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
# distanceMatricesFolder = "D:\Học\Thiết kế và đánh giá thuật toán\p-median\distanceMatrices"
# problemName = "a280"
# readDistanceMatrix(problemName, distanceMatricesFolder)    