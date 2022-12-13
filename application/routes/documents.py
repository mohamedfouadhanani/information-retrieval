from flask import Blueprint, redirect, render_template, request, make_response

import environment

documents_blueprint = Blueprint("documents", __name__)

@documents_blueprint.route("/", methods=["GET"])
def get_documents():
    if environment.configuration is None:
        return redirect("/configuration")
    
    return render_template("documents/index.html", title="Documents")

@documents_blueprint.route("/", methods=["POST"])
def post_documents():
    if environment.configuration is None:
        return redirect("/configuration")
    
    term = request.form["term"]
    # results: [[document_identifier, frequency, weight]]
    results = environment.inverse.documents(term)

    processed_results = []

    for result in results:
        document_identifier, frequency, weight = result
        document_title = environment.document_identifier_title[document_identifier]
        processed_results.append(f"{document_title}$ {frequency}$ {weight}")
        
    processed_results = "\n".join(processed_results)


    response = make_response(processed_results)
    response.headers["Content-Disposition"] = f"attachment; filename={term}_documents.csv"
    response.headers["Content-Type"] = "text/csv"

    return response