import os
import sys

sys.path.append(os.getcwd())

# typing
from typing import List

from similarity.dbscan.point import Point
from similarity.dbscan.cluster import Cluster

# FOR DEBUGING PURPOSES
from similarity.dbscan.configuration import Configuration
from inverse.inverse import Inverse
from similarity.dbscan.distances import manhattan, euclidean, minimal_distance
from similarity.dbscan.utils import show_metrics
from time import time
import numpy as np

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

def run(inverse, query, **kwargs):
    # get vars from kwargs if needed
    
    query_terms = [term.strip() for term in query.split(" ") if len(term.strip()) > 0 and term.strip() != ""]
    stemmed_query_terms = [inverse.stemmer.stem(term) for term in query_terms]

if __name__ == "__main__":
    inverse = Inverse("regextokenizer", "porter")

    p2p_distance_functions = {
        "manhattan": manhattan,
        # "euclidean": euclidean
    }
    
    configuration = Configuration(
        dataset=inverse.get_inverse_matrix(), 
        p2p_distance_functions=p2p_distance_functions.keys(),
        minimum_points=list(range(1, 6)),
        epsilons=list(range(10, 21))
    )

    possible_combinations = configuration.possible_combinations()

    n_possible_combinations = len(possible_combinations)
    print(f"n_possible_combinations = {n_possible_combinations}")

    for index, (dataset, p2p_distance_function, minimum_points, epsilon) in enumerate(possible_combinations, start=1):
        algorithm = DBSCAN(
            minimum_points=minimum_points, 
            epsilon=epsilon, 
            p2p_distance_function=p2p_distance_functions[p2p_distance_function]
        )
        
        print(f"combination {index}:")
        print(f"\tminimum points = {minimum_points}")
        print(f"\tepsilon = {epsilon}")
        print(f"\tp2p distance function = {p2p_distance_function}\n")
        
        start = time()
        clusters, outliers = algorithm(dataset=dataset)
        finish = time()

        duration = round(finish - start)

        print(f"\tdone clustering in {duration} seconds\n")

        show_metrics(clusters, outliers, manhattan, minimal_distance(manhattan), indentation="\t")
