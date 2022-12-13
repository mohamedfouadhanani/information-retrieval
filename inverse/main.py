import sys
import os
import nltk
import numpy as np
from itertools import product
from collections import Counter

# nltk.download('stopwords')

current_working_directory = os.getcwd()
sys.path.append(current_working_directory)

import environment

def weight(term, document, document_term_frequency, term_document_frequency):
    frequency = document_term_frequency[document][term]
    _, maximum_frequency_in_document = document_term_frequency[document].most_common(1)[0]

    N = len(document_term_frequency)

    documents_containig_term = [document for document, tf in term_document_frequency[term].items() if tf != 0]
    ni = len(documents_containig_term)

    tf = frequency / maximum_frequency_in_document

    idf = np.log10(N / ni + 1)

    tfidf = tf * idf

    term_weight = tfidf

    return term_weight


def populate():
    term_extraction_methods = environment.term_extraction_methods.keys()
    normalization_algorithms = environment.normalization_algorithms.keys()
    possible_configurations = product(term_extraction_methods, normalization_algorithms)

    files = os.listdir(os.path.join(".", "documents"))
    files = [file for file in files if file not in ["__init__.py", "main.py", "names.txt"]]

    files_content = {}
    for file in files:
        document_id = file.split(".")[0]
        with open(os.path.join("documents", file), "r") as input_file:
                file_content = input_file.read()
                files_content[document_id] = file_content

    all_terms = []

    stopwords = nltk.corpus.stopwords.words('english')

    regular_expression = "(?:[A-Za-z]\.)+|\d+(?:\.\d+)?%?|\w+(?:\-\w+)*"
    regex_tokenizer = nltk.RegexpTokenizer(regular_expression)

    porter_stemmer = nltk.PorterStemmer()
    lancaster_stemmer = nltk.LancasterStemmer()

    document_term_frequency = {}

    for term_extraction_method, normalization_algorithm in possible_configurations:
        print(f"starting with the combination: {term_extraction_method}, {normalization_algorithm}")
        for file in files:
            print(f"starting with the document {file}")
            # acquiring document identifier
            document_id = file.split(".")[0]

            # getting file content
            file_content = files_content[document_id]
            
            # applying the right term extraction method
            if term_extraction_method == "split":
                terms = [term.strip() for line in file_content.splitlines() for term in line.split(" ")]
            elif term_extraction_method == "regextokenizer":
                terms = regex_tokenizer.tokenize(file_content)

            # applying the right normalization method
            if normalization_algorithm == "porter":
                stemmed_terms = sorted([porter_stemmer.stem(term).lower() for term in terms if term != "" and term not in stopwords])
            elif normalization_algorithm == "lancaster":
                stemmed_terms = sorted([lancaster_stemmer.stem(term).lower() for term in terms if term != "" and term not in stopwords])
            
            all_terms += stemmed_terms
            document_term_frequency[document_id] = Counter(stemmed_terms)
            print(f"finishing with the document {file}\n")
        
        unique_terms = sorted(set(all_terms))
        print(f"there are {len(unique_terms)} unique term")
        
        term_document_frequency = {term: Counter({document: document_term_frequency[document][term] for document in document_term_frequency}) for term in unique_terms}

        print("calculating weights")
        for index, document_id in enumerate(document_term_frequency.keys(), start=1):
            for term in document_term_frequency[document_id].keys():
                computed_weight = weight(term, document_id, document_term_frequency, term_document_frequency)
                with open(os.path.join("inverse", f"{term_extraction_method}+{normalization_algorithm}+document_term.csv"), "a") as output_file:
                    output_file.write(f"{document_id}; {term}; {document_term_frequency[document_id][term]}; {computed_weight}\n")
                with open(os.path.join("inverse", f"{term_extraction_method}+{normalization_algorithm}+term_document.csv"), "a") as output_file:
                    output_file.write(f"{term}; {document_id}; {document_term_frequency[document_id][term]}; {computed_weight}\n")
            print(f"done with {index} document(s)")

        print(f"finishing with the combination: {term_extraction_method}, {normalization_algorithm}")
        print("-" * 100)

def genocide():
    files = os.listdir(os.path.join("inverse"))
    files = [file for file in files if file not in ["main.py", "__init__.py"]]
    
    for file in files:
        os.remove(os.path.join("inverse", file))

if __name__ == "__main__":
    environment.init()
    genocide()
    populate()