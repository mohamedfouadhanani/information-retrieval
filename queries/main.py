import re
import os

def populate():
    with open(os.path.join("collection", "CISI.REL"), "r") as input_file:
        file_content = input_file.read()
    
    split_file_content = file_content.splitlines()

    unique_query_identifiers = set()

    for row in split_file_content:
        row = re.split(r"\s+", row)[1:]
        query_identifier, *_ = row
        unique_query_identifiers.add(query_identifier)
    
    query_identifier_relevent_documents = {query_identifier: [] for query_identifier in unique_query_identifiers}

    for row in split_file_content:
        row = re.split(r"\s+", row)[1:]
        query_identifier, relevent_document, *_ = row
        query_identifier_relevent_documents[query_identifier].append(relevent_document)
    
    # for query_identifier, relevent_documents in query_identifier_relevent_documents.items():
    #     print(f"{query_identifier} = {relevent_documents}")
        
    # CISI.QRY
    
    with open(os.path.join("collection", "CISI.QRY")) as file:
        file_content = file.read()
    
    text_queries = re.split("\.I [0-9]*", file_content)
    text_queries = [text for text in text_queries if len(text) > 0]

    queries = {}

    condition = True
    for index, query in enumerate(text_queries, start=1):
        index = str(index)

        if ".B" in query.strip():
            raw_query = re.findall("(?<=\.W\s)[\s\S]*(?=\.B)", query)
        else:
            raw_query = re.findall("(?<=\.W\s)[\s\S]*", query)

        condition = condition and len(raw_query) == 1

        query = raw_query[0]
        processed_query = query.strip().replace("\n", " ")

        queries.update({index: processed_query})

        # print(processed_query)
        # print("-" * 100)
        # input("...")
    # print(condition)

    with open(os.path.join("queries", "index.csv"), "w") as index_file:
        for query_identifier, query_text in queries.items():
            relevent_documents_list = []

            if query_identifier in query_identifier_relevent_documents:
                relevent_documents_list = query_identifier_relevent_documents[query_identifier]
                
            relevent_documents_string = " ".join(relevent_documents_list)
            index_file.write(f"{query_identifier}$ {query_text}$ [{relevent_documents_string}]\n")

def genocide():
    files = os.listdir(os.path.join("queries"))
    files = [file for file in files if file not in ["main.py", "__init__.py"]]
    
    for file in files:
        os.remove(os.path.join("queries", file))


if __name__ == "__main__":
    genocide()
    populate()