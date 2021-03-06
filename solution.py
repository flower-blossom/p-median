def findMin(solution, distanceMatrix, p, represent):
    min = float('inf')
    for city in range(p):
        distance = distanceMatrix[solution[city], represent]
        if min > distance:
            min = distance
    return min


def getTotalDistance(solutionList, distanceMatrix, p):
    distance = 0
    for idx in range(p, len(solutionList)):
        distance += findMin(solutionList, distanceMatrix, p, solutionList[idx])
    return distance


class Solution:
    """
    Contains a list of customers and distanceMatrix
    """

    def __init__(self, solutionList, distanceMatrix, p):
        self.p = p
        self.solutionList = solutionList
        self.distanceMatrix = distanceMatrix
        self.totalDistance = getTotalDistance(
            self.solutionList, self.distanceMatrix, self.p)

    def __copy__(self):
        return self.__class__(self.solutionList.copy(), self.distanceMatrix, self.p)
