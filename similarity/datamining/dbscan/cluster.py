import os
import sys

sys.path.append(os.getcwd())

from similarity.datamining.dbscan.point import Point

from typing import List

class Cluster:
    ID = 1

    def __init__(self):
        self.points: List[Point] = []

        self.id: int = Cluster.ID
        Cluster.ID += 1

    def __equals__(self, other):
        return self.id == other.id

    def __len__(self):
        return len(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def __copy__(self):
        return Cluster(points=self.points.copy())

    def __repr__(self):
        cluster_points_string = ', '.join(map(str, self.points))
        return f"Cluster {self.id}: [{cluster_points_string}]"
    
    def append(self, point: Point):
        self.points.append(point)