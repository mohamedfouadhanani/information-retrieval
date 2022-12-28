from typing import List

class Point:
    OUTLIER = None
    UNCLUSTERED = 0
    ID = 1
    
    def __init__(self, sample):
        self.sample = sample
        self.is_visited: bool = False
        self.cluster: int = Point.UNCLUSTERED

        self.id: int = Point.ID
        Point.ID += 1
    
    def neighbors(self, points: List["Point"], epsilon: float, p2p_distance_function):
        neighboring_points = []

        for point in points:
            if point == self:
                continue

            distance = p2p_distance_function(self.sample, point.sample)
            if distance <= epsilon:
                neighboring_points.append(point)
        
        return neighboring_points
    
    def __eq__(self, other: "Point"):
        return self.id == other.id
    
    def __repr__(self):
        return f"Point {self.id}: {self.sample}"