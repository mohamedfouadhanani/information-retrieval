from itertools import product

class Configuration:
    def __init__(self, dataset, p2p_distance_functions, minimum_points, epsilons):
        self.dataset = [dataset]
        self.p2p_distance_functions = p2p_distance_functions
        self.minimum_points = minimum_points
        self.epsilons = epsilons

    def possible_combinations(self):
        result = product(self.dataset, self.p2p_distance_functions, self.minimum_points, self.epsilons)
        result = list(result)
        
        return result