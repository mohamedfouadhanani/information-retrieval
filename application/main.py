from flask import Flask, redirect

import sys
import os

os.environ["PYTHONDONTWRITEBYTECODE"] = "abc"

sys.path.append(os.getcwd())

import environment

environment.init()

# blueprints
from routes.configuration import configuration_blueprint
from routes.search import search_blueprint
from routes.document import document_blueprint
from routes.terms import terms_blueprint
from routes.documents import documents_blueprint

app = Flask(__name__)

# blueprints
app.register_blueprint(configuration_blueprint, url_prefix="/configuration")
app.register_blueprint(search_blueprint, url_prefix="/search")
app.register_blueprint(document_blueprint, url_prefix="/document")
app.register_blueprint(documents_blueprint, url_prefix="/documents")
app.register_blueprint(terms_blueprint, url_prefix="/terms")

@app.route("/", methods=["GET"])
def index():
    if environment.configuration is None:
        return redirect("/configuration")
    return redirect("/search")

if __name__ == "__main__":
    app.run(debug=True)