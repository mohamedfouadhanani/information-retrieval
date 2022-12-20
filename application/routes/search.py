from flask import Blueprint, redirect, render_template, request

import time

import environment

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/", methods=["GET"])
def get_search():
    if environment.configuration is None:
        return redirect("/configuration")
    
    documents = environment.documents
    environment.documents = []

    query = environment.query
    environment.query = ""

    duration = environment.duration
    environment.duration = None

    return render_template("search/index.html", title="Search", documents=documents, query=query, duration=duration)

@search_blueprint.route("/", methods=["POST"])
def post_search():
    if environment.configuration is None:
        return redirect("/configuration")

    query = request.form["query"]

    # print(f"running with the query \"{query}\" and similarity function {environment.configuration['rsv_function']}")

    rsv_function = environment.rsv_functions_mapping[environment.configuration["rsv_function"]]

    B = None
    K = None
    if environment.configuration["rsv_function"] == "bm25":
        B = environment.B
        K = environment.K

    start = time.time()
    results = rsv_function(inverse=environment.inverse, query=query, B=B, K=K)
    finish = time.time()

    duration = round(finish - start, environment.round_to)

    documents = []
    for document_identifier, similarity in results.items():
        if similarity == 0:
            continue
        document_title = environment.document_identifier_title[document_identifier]
        documents.append({
            "identifier": document_identifier,
            "title": document_title,
            "similarity": round(similarity, environment.round_to)
        })

    environment.documents = documents
    environment.query = query
    environment.duration = duration

    return redirect("/search")