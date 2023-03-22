import numpy as np

class Point:
    def __init__(self, weight: int, 
                 coordinate: np.ndarray, 
                 locationInDistanceMatrix: int) -> None:
        self.weight = weight
        self.coordinate = coordinate
        self.locationInDistanceMatrix = locationInDistanceMatrix
        
        