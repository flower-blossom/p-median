import numpy as np
import itertools, os

# from dataModels import Cost, Customer, DataModel
# from dataModels.Solution import Solution
# from utils import distances


def readTSPLib(fileName):
    '''Return cost and dataModel in the specific filename'''
    dataFileName = "/data/" + fileName

    with open(os.path.dirname(__file__) + dataFileName) as f_obj:
        nodeData = f_obj.readlines()

    # Get keywords
    NAME = ''
    TYPE = ''
    COMMENT = ''
    DIMENSION = 0
    EdgeWeightType = ''
    EdgeWeightFormat = ''
    DisplayDataType = ''
    DisplayDataSectionIndex = 0
    EdgeWeightSectionIndex = 0
    NodeCoordSectionIndex = 0

    for i in range(len(nodeData)):
        node = nodeData[i].split()
        if ':' in node:
            node.remove(':')
        # print(node)
        if len(node) != 0:
            if 'NAME' in node[0]:
                NAME = node[1]
            if 'TYPE' in node[0]:
                TYPE = node[1]
            if 'COMMENT' in node[0]:
                for word in node[1:]:
                    COMMENT += word + ' '
                COMMENT = COMMENT[:-1]
            if 'DIMENSION' in node[0]:
                DIMENSION = int(node[1])
            if 'EDGE_WEIGHT_TYPE' in node[0]:
                EdgeWeightType = node[1]
            if 'EDGE_WEIGHT_FORMAT' in node[0]:
                EdgeWeightFormat = node[1]
            if 'DISPLAY_DATA_TYPE' in node[0]:
                DisplayDataType = node[1]
            if 'EDGE_WEIGHT_SECTION' in node[0]:
                EdgeWeightSectionIndex = i + 1
            if 'DISPLAY_DATA_SECTION' in node[0]:
                DisplayDataSectionIndex = i + 1
            if 'NODE_COORD_SECTION' in node[0]:
                NodeCoordSectionIndex = i + 1

    dataDescription = {'NAME': NAME, 'TYPE': TYPE, 'COMMENT': COMMENT, 'DIMENSION': DIMENSION}

    # Create a dict that contains data about the nodes (id, x, y)
    NodeCoordSection = {}

    nodeStartIndex = 0
    if EdgeWeightType in ['EUC_2D', 'EUC_3D', 'MAN_2D', 'MAN_3D', 'MAX_2D', 'MAX_3D', 'GEO', 'ATT', 'CEIL_2D']:
        nodeStartIndex = NodeCoordSectionIndex
    elif EdgeWeightType == 'EXPLICIT':
        nodeStartIndex = DisplayDataSectionIndex

    # Create a dict for customers
    customersDict = {}

    if nodeStartIndex:
        while nodeStartIndex < len(nodeData) and 'EOF' not in nodeData[nodeStartIndex] and nodeData[nodeStartIndex] != '':
            if ' ' in nodeData[nodeStartIndex]:
                customerData = nodeData[nodeStartIndex].split(' ')
            elif '\t' in nodeData[nodeStartIndex]:
                customerData = nodeData[nodeStartIndex].split('\t')
            customerData = [i for i in customerData if i != '' and i != '\n']
            customerData[-1] = customerData[-1][:-1]
            
            if EdgeWeightType == 'GEO':
                NodeCoordSection[int(customerData[0])] = {'lat': getLatitude(float(customerData[1])), 
                                                    'lon': getLongitude(float(customerData[2]))}
            else:
                NodeCoordSection[int(customerData[0])] = {'lat': float(customerData[1]), 'lon': float(customerData[2])}
            nodeStartIndex += 1

        for node in NodeCoordSection:
            customersDict[f'Customer {node-1}'] = Customer(node-1, NodeCoordSection[node])
    else:
        for i in range(DIMENSION):
            customersDict[f'Customer {i}'] = Customer(str(i), {'lat': 'na', 'lon': 'na'})


    # Create a numpy array for the distance matrix
    distancesMatrix = np.zeros((DIMENSION, DIMENSION))

    if EdgeWeightType == 'EXPLICIT':
        # a numpy array representing the distances matrix
        distancesMatrix = np.zeros((DIMENSION, DIMENSION))

        # List contains all distances data numbers in order
        distanceDataList = []

        # index of the first row of data
        distancesStartIndex = EdgeWeightSectionIndex
        
        # read the data into the distanceDataList
        while 'DISPLAY_DATA_SECTION' not in nodeData[distancesStartIndex] and 'EOF' not in nodeData[distancesStartIndex]:
            rowData = nodeData[distancesStartIndex].split(' ')
            rowData = [num for num in rowData if num != '' and num != '\n']
            distanceDataList += rowData
            distancesStartIndex += 1

        if EdgeWeightFormat == 'FULL_MATRIX':
            for i in range(DIMENSION):
                for j in range(i, DIMENSION):
                    distancesMatrix[i, j] = distanceDataList[i*DIMENSION + j]
                    distancesMatrix[j, i] = distancesMatrix[i, j]

        if EdgeWeightFormat == 'UPPER_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(DIMENSION - 1 - i):
                    distancesMatrix[i, i + 1 + j] = distanceDataList[dataCount]
                    dataCount += 1
            # distancesMatrix = np.fliplr(distancesMatrix)
            for i, j in itertools.combinations_with_replacement(range(DIMENSION-1, -1, -1), 2):
                distancesMatrix[i, j] = distancesMatrix[j, i]

        if EdgeWeightFormat == 'LOWER_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(i):
                    distancesMatrix[i, j] = distanceDataList[dataCount]
                    dataCount += 1
            for i, j in itertools.combinations_with_replacement(range(DIMENSION), 2):
                distancesMatrix[i, j] = distancesMatrix[j, i]

        if EdgeWeightFormat == 'UPPER_DIAG_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(DIMENSION - i):
                    distancesMatrix[i, i + j] = distanceDataList[dataCount]
                    dataCount += 1
            # distancesMatrix = np.fliplr(distancesMatrix)
            for i, j in itertools.combinations_with_replacement(range(DIMENSION-1, -1, -1), 2):
                distancesMatrix[i, j] = distancesMatrix[j, i]

        if EdgeWeightFormat == 'LOWER_DIAG_ROW':
            dataCount = 0
            for i in range(DIMENSION):
                for j in range(i+1):
                    distancesMatrix[i, j] = distanceDataList[dataCount]
                    dataCount += 1
            for i, j in itertools.combinations_with_replacement(range(DIMENSION), 2):
                distancesMatrix[i, j] = distancesMatrix[j, i]
    else:
        distancesMatrix = np.zeros((DIMENSION, DIMENSION))
        for i, j in itertools.product(range(DIMENSION), repeat = 2):
            distancesMatrix[i, j] = getDistance(customersDict[f'Customer {i}'], 
            customersDict[f'Customer {j}'], EdgeWeightType)
    # cost = Cost.Cost(distancesMatrix)
    # dataModel = DataModel.DataModel(customersDict, dataDescription)
    return customersDict


import math

EARTH_RADIUS = 6378.388
PI = 3.141592

def getDistance(customer1, customer2, edgeWeightType):
    '''Return distance between two customers'''
    d = 0
    if customer1 == customer2:
        return d
    elif edgeWeightType == 'EUC_2D':
        d = getEUC2DDistance(customer1, customer2)
    elif edgeWeightType == 'MAN_2D':
        d = getMAN2DDistance(customer1, customer2)
    elif edgeWeightType == 'MAX_2D':
        d = getMAX2DDistance(customer1, customer2)
    elif edgeWeightType == 'GEO':
        d = getGEODistance(customer1, customer2)
    elif edgeWeightType == 'ATT':
        d = getATTDistance(customer1, customer2)
    elif edgeWeightType == 'CEIL_2D':
        d = getCEIL2DDistance(customer1, customer2)
    return d

def getEUC2DDistance(customer1, customer2):
    squared_dx = (getDX(customer1, customer2))**2
    squared_dy = (getDY(customer1, customer2))**2
    d = math.sqrt(squared_dx + squared_dy)
    return int(d + 0.5)

def getMAN2DDistance(customer1, customer2):
    dx = abs(getDX(customer1, customer2))
    dy = abs(getDY(customer1, customer2))
    d = dx + dy
    return int(d + 0.5)

def getMAX2DDistance(customer1, customer2):
    dx = abs(getDX(customer1, customer2))
    dy = abs(getDY(customer1, customer2))
    return max(int(dx + 0.5), int(dy + 0.5))

def getGEODistance(customer1, customer2):
    q1 = math.cos(getDY(customer1, customer2))
    q2 = math.cos(getDX(customer1, customer2))
    q3 = math.cos(customer1.coordinate['lat'] + customer2.coordinate['lat'])
    return int(EARTH_RADIUS * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

def getATTDistance(customer1, customer2):
    dx = getDX(customer1, customer2)
    dy = getDY(customer1, customer2)
    r = math.sqrt((dx**2 + dy**2) / 10.0)
    t = int(r + 0.5)
    if t < r:
        return t + 1
    return t

def getCEIL2DDistance(customer1, customer2):
    squaredDx = (getDX(customer1, customer2))**2
    squaredDy = (getDY(customer1, customer2))**2
    d = math.sqrt(squaredDx + squaredDy)
    return math.ceil(d)

def getDX(customer1, customer2):
    '''Return x-distance of two customers'''
    return customer1.coordinate['lat'] - customer2.coordinate['lat']

def getDY(customer1, customer2):
    '''Return y-distance of two customers'''
    return customer1.coordinate['lon'] - customer2.coordinate['lon']

# def getDZ(customer1, customer2):
#     '''Return z-distance of two customers'''
#     return customer1.coordinate[2] - customer2.coordinate[2]

def getLatitude(xCoordinate):
    '''Return converted-latitude of the x coordinate'''
    deg = int(xCoordinate)
    min = xCoordinate - deg
    latitude = PI * (deg + 5.0 * min / 3.0) / 180.0
    return latitude

def getLongitude(yCoordinate):
    '''Return converted-longitude of the y coordinate'''
    deg = int(yCoordinate)
    min = yCoordinate - deg
    longitude = PI * (deg + 5.0 * min / 3.0) / 180.0
    return longitude

### Customers class

class Customer():
    '''A class representing a customer'''

    def __init__(self, id, coordinate):
        self.id = id
        self.coordinate = coordinate

    def __repr__(self):
        return f'Customer ID: {self.id}, Latitude: {self.coordinate["lat"]}, Longitude: {self.coordinate["lon"]}.'