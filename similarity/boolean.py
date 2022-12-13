import numpy as np

import os
import sys

sys.path.append(os.getcwd())

from inverse.inverse import Inverse

def run(inverse, query, **kwargs):
    vectorizer = Vectorizer(inverse=inverse)
    query_parser = QueryParser(vectorizer=vectorizer)

    parsed_query = query_parser(query)
        
    is_correct = query_parser.check(parsed_query=parsed_query)

    if not is_correct:
        return {}
    
    result_boolean_vector = query_parser.evaluate(parsed_query=parsed_query)

    documents = vectorizer.reverse(result_boolean_vector)
    documents = {document: 1 for document in documents}

    return documents


class Vectorizer:
    def __init__(self, inverse):
        self.inverse = inverse

    def __call__(self, term):
        stemmed_term = self.inverse.stemmer.stem(term)

        n_docs = len(self.inverse.unique_documents)
        
        if stemmed_term not in self.inverse.unique_terms:
            boolean_vector = np.zeros((n_docs, ), dtype=np.int64)
            return boolean_vector
        
        boolean_vector = np.array([1 if self.inverse.frequency(document=document, term=stemmed_term) > 0 else 0 for document in self.inverse.unique_documents], dtype=np.int64)

        return boolean_vector
    
    def reverse(self, boolean_vector):
        np_unique_documents = np.array(list(self.inverse.unique_documents), dtype="object")

        documents = [document for document in boolean_vector * np_unique_documents if document != ""]

        return documents

    
    @classmethod
    def AND(cls, boolean_vector_1, boolean_vector_2):
        result_boolean_vector = (boolean_vector_1 * boolean_vector_2).astype(np.int64)
        return result_boolean_vector

    @classmethod
    def OR(cls, boolean_vector_1, boolean_vector_2):
        result_boolean_vector = ((boolean_vector_1 + boolean_vector_2) > 0).astype(np.int64)
        return result_boolean_vector

    @classmethod
    def NOT(cls, boolean_vector):
        result_boolean_vector = np.logical_not(boolean_vector).astype(np.int64)
        return result_boolean_vector


class QueryParser:
    def __init__(self, vectorizer):
        self.precedence = {
            "not": 3,
            "and": 2,
            "or": 1
        }

        self.operators = self.precedence.keys()

        self.vectorizer = vectorizer

    def __call__(self, query):
        query = query.lower()
        query = query.replace("(", " ( ")
        query = query.replace(")", " ) ")
        query = query.split(" ")
        
        tokens = [token.strip() for token in query if len(token.strip()) > 0 and token.strip() != ""]

        stack = []
        queue = []

        for token in tokens:

            if token in self.operators:
                while stack:
                    tos = stack[-1]
                    if tos in self.operators and self.precedence[tos] <= self.precedence[token] or tos == "(":
                        break
                    tos = stack.pop()
                    queue.append(tos)
                stack.append(token)
                continue

            if token == "(":
                stack.append(token)
                continue

            if token == ")":
                while stack:
                    tos = stack[-1]
                    if tos == "(":
                        break
                    tos = stack.pop()
                    queue.append(tos)
                tos = stack[-1]

                if tos != "(":
                    return []

                tos = stack.pop()
                continue

            queue.append(token)

        while stack:
            tos = stack.pop()
            if tos == "(":
                return []
            queue.append(tos)

        return queue
    
    def evaluate(self, parsed_query):
        stack = []
        for token in parsed_query:
            if token == "not":
                tos = stack.pop()
                result = Vectorizer.NOT(tos)
                stack.append(result)
                continue
            
            if token == "and":
                tos_1 = stack.pop()
                tos_2 = stack.pop()
                result = Vectorizer.AND(tos_1, tos_2)
                stack.append(result)
                continue

            if token == "or":
                tos_1 = stack.pop()
                tos_2 = stack.pop()
                result = Vectorizer.OR(tos_1, tos_2)
                stack.append(result)
                continue

            # token is not and operator
            boolean_vector = self.vectorizer(token)
            stack.append(boolean_vector) # or append its boolean representation
        
        result = stack.pop()

        return result

    def check(self, parsed_query):       
        stack = []
        
        for token in parsed_query:
            try:
                if token == "not":
                    tos = stack.pop()
                    result = f"not{tos}"
                    stack.append(result)
                    continue

                if token == "and":
                    tos_1 = stack.pop()
                    tos_2 = stack.pop()
                    result = f"{tos_1}and{tos_2}"
                    stack.append(result)
                    continue

                if token == "or":
                    tos_1 = stack.pop()
                    tos_2 = stack.pop()
                    result = f"{tos_1}ors{tos_2}"
                    stack.append(result)
                    continue
                
                stack.append(token)
            except:
                return False

        stack_length = len(stack)

        if stack_length == 1:
            return True
        
        return False
        

if __name__ == "__main__":
    inverse = Inverse("regextokenizer", "porter")
    vectorizer = Vectorizer(inverse=inverse)
    query_parser = QueryParser(vectorizer=vectorizer)
    
    query = "networks neural deep learning"
    
    parsed_query = query_parser(query)
    print(f"parsed_query = {parsed_query}")

    is_correct = query_parser.check(parsed_query)
    print(f"check(parsed_query) = {is_correct}")
    
    # results = run(inverse, query)
    
    # print("results")
    # print(results)