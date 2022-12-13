from flask import Blueprint, redirect, render_template, request
import os

from inverse.inverse import Inverse

import environment

configuration_blueprint = Blueprint("configuration", __name__)

@configuration_blueprint.route("/", methods=["GET"])
def get_configuration():
    environment.configuration = None

    configurations = environment.configurations

    return render_template("configuration/index.html", title="Configuration", configurations=configurations)

@configuration_blueprint.route("/", methods=["POST"])
def post_configuration():
    if environment.configuration is not None:
        return redirect("/search")
    
    configuration = {}
    
    for _, environment_configuration in environment.configurations.items():
        variable_name = environment_configuration["variable_name"]
        variable_value = request.form[variable_name]
        configuration.update({variable_name: variable_value})
    
    environment.configuration = configuration

    if environment.configuration["rsv_function"] == "bm25":
        environment.B = float(request.form["B"])
        environment.K = float(request.form["K"])

    environment.inverse = Inverse(
        extraction_method=environment.configuration["term_extraction_method"],
        normalization_algorithm=environment.configuration["normalization_algorithm"]
    )

    environment.document_identifier_title = {}
    environment.document_title_identifier = {}

    with open(os.path.join("documents", "names.txt"), "r") as names_file:
        names_file_content = names_file.read()
        names_file_content = names_file_content.splitlines()

    for row in names_file_content:
        identifier, title = row.split("$ ")
        environment.document_identifier_title.update({identifier: title})
        environment.document_title_identifier.update({title: identifier})
    
    return redirect("/search")