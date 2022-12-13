import numpy as np

from time import time
from collections import Counter

import os
import sys

sys.path.append(os.getcwd())

from inverse.inverse import Inverse

def rsv(inverse, document, stemmed_query_terms, B, K):
    N = len(inverse.unique_documents)
    
    summation = 0
    for stemmed_query_term in stemmed_query_terms:
        
        if stemmed_query_term not in inverse.unique_terms:
            summation += 0
            continue

        frequency = inverse.frequency(document=document, term=stemmed_query_term)

        documents_containig_term = [document for document, tf in inverse.document_frequency_given_term(stemmed_query_term).items() if tf != 0]
        ni = len(documents_containig_term)

        tf = frequency / (K * ((1 - B) + B * inverse.document_length[document] / inverse.average_document_length) + frequency)

        idf = np.log10((N - ni + 0.5) / (ni + 0.5))

        tfidf = tf * idf
        summation += tfidf
    
    return tfidf

def run(inverse, query, **kwargs):
    B = kwargs["B"]
    K = kwargs["K"]

    query_terms = [term.strip() for term in query.split(" ") if len(term.strip()) > 0 and term.strip() != ""]
    stemmed_query_terms = [inverse.stemmer.stem(term) for term in query_terms]
    
    document_similarity = {}

    for index, document in enumerate(inverse.unique_documents, start=1):
        similarity = rsv(inverse, document, stemmed_query_terms, B, K)
        document_similarity[document] = similarity
        # print(f"done with {index} documents")
    
    document_similarity = {document: similarity for document, similarity in sorted(document_similarity.items(), key=lambda x: x[1], reverse=True)}
        
    return document_similarity

if __name__ == "__main__":
    inverse = Inverse("regextokenizer", "porter")
    query = "results query graph system"
    start = time()
    results = run(inverse, query, B=0.5, K=1.2)
    finish = time()

    print(f"done within {finish - start} seconds")
    
    print("results")
    print(results)