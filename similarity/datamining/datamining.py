import os
import sys

sys.path.append(os.getcwd())

from similarity.datamining.dbscan.dbscan import DBSCAN
from similarity.datamining.dbscan.configuration import Configuration
from inverse.inverse import Inverse
from similarity.datamining.dbscan.distances import manhattan, euclidean, minimal_distance
from similarity.datamining.dbscan.utils import show_metrics
from time import time
import numpy as np

def run(inverse, query, **kwargs):
    # get vars from kwargs if needed
    clusters = kwargs["clusters"]
    outliers = kwargs["outliers"]
    
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
