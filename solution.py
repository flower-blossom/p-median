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
        for i, j in zip(self.customerList, self.customerList[1:] + [self.customerList[0]]):
            distance += self.distanceMatrix[i, j]
        return distance

