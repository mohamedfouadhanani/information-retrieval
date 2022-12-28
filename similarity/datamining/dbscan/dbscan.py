import os
import sys

sys.path.append(os.getcwd())

# typing
from typing import List

from similarity.datamining.dbscan.point import Point
from similarity.datamining.dbscan.cluster import Cluster

class DBSCAN:
    def __init__(self, minimum_points, epsilon, p2p_distance_function):
        self.minimum_points: int = minimum_points
        self.epsilon: float = epsilon
        self.p2p_distance_function = p2p_distance_function
    
    def __call__(self, dataset):
        points: List[Point] = [Point(sample=point) for point in dataset]
        cluster: int = 0

        for point in points:
            if point.is_visited:
                continue
                
            point.is_visited = True
            neighbors: List[Point] = point.neighbors(
                points=points, 
                epsilon=self.epsilon,
                p2p_distance_function=self.p2p_distance_function
            )

            n_neighbors: int = len(neighbors)
            if n_neighbors < self.minimum_points:
                point.cluster = Point.OUTLIER
            else:
                cluster += 1
                self.extend_cluster(points=points, point=point, neighbors=neighbors, cluster=cluster)
        
        # construct clusters
        clusters: List[Cluster] = [Cluster() for _ in range(cluster)]
        outliers: List[Point] = []

        for point in points:
            if point.cluster == Point.OUTLIER:
                outliers.append(point)
                continue
            clusters[point.cluster - 1].append(point)

        return clusters, outliers

    def extend_cluster(self, points: List[Point], point: Point, neighbors: List[Point], cluster: int):
        point.cluster = cluster

        for neighbor in neighbors:
            if not neighbor.is_visited:
                neighbor.is_visited = True
                neighbor_neighbors = neighbor.neighbors(
                    points=points, 
                    epsilon=self.epsilon,
                    p2p_distance_function=self.p2p_distance_function
                )

                n_neighbors = len(neighbor_neighbors)
                if n_neighbors >= self.minimum_points:
                    neighbors.extend(neighbor_neighbors)
            
            if neighbor.cluster == Point.UNCLUSTERED:
                neighbor.cluster = cluster
