import os
import sys
import nltk
import numpy as np

from time import time

current_working_directory = os.getcwd()
sys.path.append(current_working_directory)

class Inverse:
    def __init__(self, extraction_method, normalization_algorithm):
        self.extraction_method = extraction_method
        self.normalization_algorithm = normalization_algorithm
        self.unique_documents = set()
        self.unique_terms = set()

        if self.normalization_algorithm == "porter":
            self.stemmer = nltk.PorterStemmer()
        elif self.normalization_algorithm == "lancaster":
            self.stemmer = nltk.LancasterStemmer()

        with open(os.path.join("inverse", f"{self.extraction_method}+{self.normalization_algorithm}+document_term.csv"), "r") as document_term_inverse_file:
            document_term_inverse = document_term_inverse_file.read()
        
        # read unique document names and terms
        for row in document_term_inverse.splitlines():
            document, term, frequency, weight = row.split("; ")
            self.unique_documents.add(document)
            self.unique_terms.add(term)
        
        self.document_index_mapping = {document: index for index, document in enumerate(self.unique_documents)}
        self.term_index_mapping = {term: index for index, term in enumerate(self.unique_terms)}

        # inverse matrix initialization
        n_docs = len(self.unique_documents)
        n_terms = len(self.unique_terms)

        self.inverse_matrix = np.zeros((n_docs, n_terms))
        
        # document term (frequency / weight)
        self.document_term_frequency = {document: {} for document in self.unique_documents}
        self.document_term_weight = {document: {} for document in self.unique_documents}

        self.wj_squared_sum = {document: 0 for document in self.unique_documents}
        self.document_length = {document: 0 for document in self.unique_documents}

        for row in document_term_inverse.splitlines():
            document, term, frequency, weight = row.split("; ")
            frequency = int(frequency)
            weight = float(weight)
            
            self.document_term_frequency[document].update({term: frequency})
            self.document_term_weight[document].update({term: weight})

            self.wj_squared_sum[document] += weight ** 2
            self.document_length[document] += frequency

            document_index = self.document_index_mapping[document]
            term_index = self.term_index_mapping[term]

            self.inverse_matrix[document_index, term_index] = weight
        
        self.average_document_length = sum(self.document_length.values()) / len(self.unique_documents)
        
        # term document (frequency / weight)
        with open(os.path.join("inverse", f"{self.extraction_method}+{self.normalization_algorithm}+term_document.csv"), "r") as term_document_inverse_file:
            term_document_inverse = term_document_inverse_file.read()
        
        self.term_document_frequency = {term: {} for term in self.unique_terms}
        self.term_document_weight = {term: {} for term in self.unique_terms}

        for row in term_document_inverse.splitlines():
            term, document, frequency, weight = row.split("; ")
            self.term_document_frequency[term].update({document: int(frequency)})
            self.term_document_weight[term].update({document: float(weight)})
        
    
    def weight(self, document, term):
        term = self.stemmer.stem(term)

        if document in self.document_term_weight and term in self.document_term_weight[document]:
            return self.document_term_weight[document][term]

        return 0


    def frequency(self, document, term):
        term = self.stemmer.stem(term)

        if document in self.document_term_frequency and term in self.document_term_frequency[document]:
            return self.document_term_frequency[document][term]

        return 0
    
    
    def terms(self, document_identifier):
        if document_identifier not in self.document_term_frequency:
            return ""
        
        term_frequency = self.document_term_frequency[document_identifier]
        term_weight = self.document_term_weight[document_identifier]
        term_frequency_weight = {term: {"frequency": term_frequency[term], "weight": term_weight[term]} for term in term_frequency}

        results = ""
        for term, frequency_weight_dictionary in term_frequency_weight.items():
            frequency = frequency_weight_dictionary["frequency"]
            weight = frequency_weight_dictionary["weight"]
            results += f"{term}$ {frequency}$ {weight}\n"
        
        return results
        
    def documents(self, term):
        term = self.stemmer.stem(term)

        if term not in self.term_document_frequency:
            return []
        
        document_frequency = self.term_document_frequency[term]
        document_weight = self.term_document_weight[term]
        document_frequency_weight = {
            document: {"frequency": document_frequency[document], "weight": document_weight[document]} 
            for document in document_frequency
        }

        results = []
        for document, frequency_weight_dictionary in document_frequency_weight.items():
            frequency = frequency_weight_dictionary["frequency"]
            weight = frequency_weight_dictionary["weight"]
            results.append([document, frequency, weight])
        
        return results
    
    def document_frequency_given_term(self, stemmed_term):
        if stemmed_term not in self.unique_terms:
            return {document: 0 for document in self.unique_documents}
        
        return self.term_document_frequency[stemmed_term]
    
    def get_inverse_matrix(self):
        return self.inverse_matrix


if __name__ == "__main__":
    start = time()
    inverse = Inverse(extraction_method="split", normalization_algorithm="lancaster")
    finish = time()

    duration = round(finish - start)

    print(f"done loading inverse file in {duration} seconds")
    
    # print(inverse.weight(document="1", term="dewey"))
    # print(inverse.get_inverse_matrix())