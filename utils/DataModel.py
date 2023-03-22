class DataModel:
    '''
    Contains lists about description of problem
    '''
    def __init__(self, quantityOfPoint, weightCluster, 
                 weightOfPoints, weightOfVehicle, typeOfPoint,
                 depot):
        self.depot = depot - 1
        self.typeOfPoint = typeOfPoint 
        self.quantityOfPoint = quantityOfPoint
        self.weightCluster = weightCluster
        self.weightOfPoints = weightOfPoints
        self.weightOfVehicle = weightOfVehicle
