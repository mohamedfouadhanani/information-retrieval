from flask import Blueprint, render_template, redirect, request, make_response
import os

import environment

terms_blueprint = Blueprint("terms", __name__)

@terms_blueprint.route("/", methods=["GET"])
def get_terms():
    if environment.configuration is None:
        return redirect("/configuration")
    
    return render_template("terms/index.html", title="Terms")

@terms_blueprint.route("/", methods=["POST"])
def post_terms():
    if environment.configuration is None:
        return redirect("/configuration")
    
    document_name = request.form["document"]
    # document exists
    if document_name not in environment.document_title_identifier:
        return redirect("/terms")
    # document identifier
    document_identifier = environment.document_title_identifier[document_name]
    # call function
    results = environment.inverse.terms(document_identifier)

    response = make_response(results)
    response.headers["Content-Disposition"] = f"attachment; filename={document_identifier}_terms.csv"
    response.headers["Content-Type"] = "text/csv"

    return response