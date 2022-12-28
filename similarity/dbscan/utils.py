import os
import sys

sys.path.append(os.getcwd())

from matplotlib import pyplot as plt
import colorsys

from similarity.dbscan.cluster import Cluster
from similarity.dbscan.point import Point

from typing import List

from similarity.dbscan.metrics import interclusters_distance, intraclusters_distance

def HSVToRGB(h, s, v): 
	(r, g, b) = colorsys.hsv_to_rgb(h, s, v) 
	return (r, g, b)
 
def get_distinct_colors(n): 
	huePartition = 1.0 / (n + 1) 
	return [HSVToRGB(huePartition * value, 1.0, 1.0) for value in range(0, n)]

def show_clusters(clusters: List[Cluster], outliers: List[Point], title="DBSCAN Clustering algorithm"):
	n_clusters = len(clusters)
	colors = get_distinct_colors(n_clusters)

	for color_index, cluster in enumerate(clusters):
		X = [point.sample[0] for point in cluster.points]
		Y = [point.sample[1] for point in cluster.points]
		
		color = colors[color_index]
		plt.scatter(X, Y, color=color, label=f"cluster with id {cluster.id}")
	

	X = [outlier.sample[0] for outlier in outliers]
	Y = [outlier.sample[1] for outlier in outliers]
	
	plt.scatter(X, Y, color="k", label="outliers")
	

	plt.title(title)
	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
	plt.tight_layout()
	plt.show()

def show_metrics(clusters, outliers, p2p_distance_function, c2c_distance_function, indentation=""):
	measure_1 = intraclusters_distance(clusters, p2p_distance_function)
	measure_2 = interclusters_distance(clusters, c2c_distance_function)
	measure_3 = len(clusters)
	measure_4 = len(outliers)

	print(f"{indentation}measure 1 (intra-clusters distance): {measure_1}")
	print(f"{indentation}measure 2 (inter-clusters distance): {measure_2}")
	print(f"{indentation}measure 3 (number of clusters): {measure_3}")
	print(f"{indentation}measure 4 (number of outliers): {measure_4}")