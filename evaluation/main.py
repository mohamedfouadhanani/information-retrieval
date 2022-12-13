import os
import sys

sys.path.append(os.getcwd())

from similarity.scalar import run as run_scalar
from similarity.cosine import run as run_cosine
from similarity.jaccard import run as run_jaccard
from similarity.bm25 import run as run_bm25

from inverse.inverse import Inverse

from utils import precision_at, recall_at, precision, recall, f_measure, precision_interpolation

configurations = [
    {
        "name": "scalar",
        "function": run_scalar,
        "params": None
    },
    {
        "name": "cosine",
        "function": run_cosine,
        "params": None
    },
    {
        "name": "jaccard",
        "function": run_jaccard,
        "params": None
    },
    {
        "name": "bm25",
        "function": run_bm25,
        "params": [(1.2, 0.5), (2.0, 0.75)]
    },
]

def main():
    inverse = Inverse(extraction_method="regextokenizer", normalization_algorithm="lancaster")

    with open(os.path.join("queries", "index.csv"), "r") as file:
        file_content = file.read()
    
    queries = []
    
    split_file_content = [query.split("$ ") for query in file_content.splitlines()]
    for query in split_file_content:
        query_identifier, query_text, string_relevent_documents = query

        relevent_documents = string_relevent_documents.replace("[", "").replace("]", "")

        if relevent_documents == "":
            relevent_documents = None
        else:
            relevent_documents = relevent_documents.split(" ")

        query = {
            "query_identifier": query_identifier,
            "query_text": query_text,
            "relevent_documents": relevent_documents
        }

        queries.append(query)
    
    # with open(os.path.join("evaluation", "index_1.csv"), "w") as file:
    #     file.write(f"rsv$ query identifier$ p@5$ p@10$ recall$ f_measure$ precision interpolation\n")
    
    # with open(os.path.join("evaluation", "index_2.csv"), "w") as file:
    #     params = configurations[-1]["params"].keys()
        
    #     params_string = "$ ".join(params)
        
    #     file.write(f"rsv$ {params_string}$ query identifier$ p@5$ p@10$ recall$ f_measure$ precision interpolation\n")

    # for configuration in configurations:
    #     name = configuration["name"]
    #     function = configuration["function"]
    #     params = configuration["params"]

    #     if params is not None:
    #         continue

    #     for query in queries:
    #         query_identifier = query["query_identifier"]
    #         query_text = query["query_text"]
    #         relevent_documents = query["relevent_documents"]

    #         print(f"function = {name}, query = {query_identifier}")
            
    #         # p@5, p@10, rappel, f-measure
    #         documents_similarity = function(inverse, query_text)
    #         selected_documents = [document for document, similarity in documents_similarity.items() if similarity > 0]
            
    #         p_at_5 = precision_at(5, selected_documents, relevent_documents)
    #         p_at_10 = precision_at(10, selected_documents, relevent_documents)

    #         r_at_10 = recall_at(10, selected_documents, relevent_documents)
            
    #         query_recall = recall(selected_documents, relevent_documents)
    #         query_precision = precision(selected_documents, relevent_documents)
    #         query_f_measure = f_measure(query_recall, query_precision)

    #         precision_recall_at_10 = zip(p_at_10, r_at_10)
    #         interpolated_precision_at_10 = precision_interpolation(precision_recall_at_10)
    #         precision_values = [precision for _, precision in interpolated_precision_at_10]

    #         if not p_at_5:
    #             string_p_at_5 = "None"
    #         else:
    #             string_p_at_5 = ", ".join(map(str, p_at_5))
            
    #         if not p_at_10:
    #             string_p_at_10 = "None"
    #         else:
    #             string_p_at_10 = ", ".join(map(str, p_at_10))
            
    #         if not precision_values:
    #             string_precision_values = "None"
    #         else:
    #             string_precision_values = ", ".join(map(str, precision_values))

    #         with open(os.path.join("evaluation", "index_1.csv"), "a") as file:
    #             file.write(f"{name}$ {query_identifier}$ {string_p_at_5}$ {string_p_at_10}$ {query_recall}$ {query_f_measure}$ {string_precision_values}\n")
    
    configuration = configurations[-1]
    name = configuration["name"]
    function = configuration["function"]
    params = configuration["params"]

    for K, B in params:
        for query in queries:
            query_identifier = query["query_identifier"]
            query_text = query["query_text"]
            relevent_documents = query["relevent_documents"]

            print(f"function = {name}, query = {query_identifier}, K = {K}, B = {B}")
            
            # p@5, p@10, rappel, f-measure
            documents_similarity = function(inverse, query_text, K=K, B=B)
            selected_documents = [document for document, similarity in documents_similarity.items() if similarity > 0]
            
            p_at_5 = precision_at(5, selected_documents, relevent_documents)
            p_at_10 = precision_at(10, selected_documents, relevent_documents)

            r_at_10 = recall_at(10, selected_documents, relevent_documents)
            
            query_recall = recall(selected_documents, relevent_documents)
            query_precision = precision(selected_documents, relevent_documents)
            query_f_measure = f_measure(query_recall, query_precision)

            precision_recall_at_10 = zip(p_at_10, r_at_10)
            interpolated_precision_at_10 = precision_interpolation(precision_recall_at_10)
            precision_values = [precision for _, precision in interpolated_precision_at_10]

            if not p_at_5:
                string_p_at_5 = "None"
            else:
                string_p_at_5 = ", ".join(map(str, p_at_5))
            
            if not p_at_10:
                string_p_at_10 = "None"
            else:
                string_p_at_10 = ", ".join(map(str, p_at_10))
            
            if not precision_values:
                string_precision_values = "None"
            else:
                string_precision_values = ", ".join(map(str, precision_values))

            with open(os.path.join("evaluation", "index_1.csv"), "a") as file:
                file.write(f"{name}$ {query_identifier}$ {string_p_at_5}$ {string_p_at_10}$ {query_recall}$ {query_f_measure}$ {string_precision_values}\n")
    

            

if __name__ == "__main__":
    main()