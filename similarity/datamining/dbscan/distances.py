import numpy as np

def manhattan(point_1, point_2):
    distance = np.sum(np.abs(point_1 - point_2))
    return distance


def euclidean(point_1, point_2):
    distance = np.sqrt(np.sum((point_1 - point_2) ** 2))
    return distance

def minimal_distance(distance_function):
    def compute_distance(cluster_1, cluster_2):
        """computes the minimal distance between two clusters"""
        minimal_distance = float("+inf")

        for point_1 in cluster_1.points:
            for point_2 in cluster_2.points:
                distance = distance_function(point_1.sample, point_2.sample)

                if distance < minimal_distance:
                    minimal_distance = distance

        return minimal_distance
    
    return compute_distance