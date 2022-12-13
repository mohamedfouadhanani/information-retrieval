import numpy as np

import os
import sys

sys.path.append(os.getcwd())

from inverse.inverse import Inverse

def rsv(inverse, document, stemmed_query_terms):
    equation_1 = sum([inverse.weight(document=document, term=term) for term in stemmed_query_terms])
    equation_2 = len(stemmed_query_terms)
    equation_3 = inverse.wj_squared_sum[document]

    results = equation_1 / (equation_2 + equation_3 - equation_1)
    
    return results

def run(inverse, query, **kwargs):
    query_terms = [term.strip() for term in query.split(" ") if len(term.strip()) > 0 and term.strip() != ""]
    stemmed_query_terms = [inverse.stemmer.stem(term) for term in query_terms]
    
    document_similarity = {}

    for index, document in enumerate(inverse.unique_documents, start=1):
        similarity = rsv(inverse, document, stemmed_query_terms)
        document_similarity[document] = similarity
        # print(f"done with {index} documents")
        
    document_similarity = {document: similarity for document, similarity in sorted(document_similarity.items(), key=lambda x: x[1], reverse=True)}
        
    return document_similarity

if __name__ == "__main__":
    inverse = Inverse("regextokenizer", "porter")
    query = "results query graph system"
    results = run(inverse, query)
    
    print("results")
    print(results)