from similarity.scalar import run as run_scalar
from similarity.cosine import run as run_cosine
from similarity.jaccard import run as run_jaccard
from similarity.boolean import run as run_boolean
from similarity.bm25 import run as run_bm25
from similarity.dbscan.dbscan import run as run_datamining

def init():
    global round_to
    round_to = 5
    
    global term_extraction_methods
    term_extraction_methods = {
        "split": "split function",
        "regextokenizer": "regular expression tokenizer"
    }

    global normalization_algorithms
    normalization_algorithms = {
        "porter": "porter stemmer",
        "lancaster": "lancaster stemmer"
    }

    global rsv_functions
    rsv_functions = {
        "scalar": "scalar product",
        "cosine": "cosine measure",
        "Jaccard": "jaccard measure",
        "boolean": "boolean",
        "bm25": "BM25",
        "datamining": "data mining"
    }

    global configurations
    configurations = {
        "term extraction methods": {
            "variable_name": "term_extraction_method",
            "options": term_extraction_methods
        },
        "normalization algorithms": {
            "variable_name": "normalization_algorithm",
            "options": normalization_algorithms
        },
        "retrieval status value functions": {
            "variable_name": "rsv_function",
            "options": rsv_functions
        }
    }
    
    global documents
    documents = []

    global query
    query = ""

    global duration
    duration = None
    
    global configuration
    configuration = None

    global rsv_functions_mapping
    rsv_functions_mapping = {
        "scalar": run_scalar,
        "cosine": run_cosine,
        "Jaccard": run_jaccard,
        "boolean": run_boolean,
        "bm25": run_bm25,
        "datamining": run_datamining
    }

if __name__ == "__main__":
    pass