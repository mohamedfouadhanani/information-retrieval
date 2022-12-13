from flask import Blueprint, redirect, render_template, request

import os

import environment

document_blueprint = Blueprint("document", __name__)

@document_blueprint.route("/<string:id>", methods=["GET"])
def get_document(id):
    if id not in environment.document_identifier_title:
        return redirect("/search")
    
    title = environment.document_identifier_title[id]
    
    with open(os.path.join("documents", f"{id}.txt"), "r") as document:
        document_content = document.read()
    
    return render_template("document/index.html", title=title, content=document_content)