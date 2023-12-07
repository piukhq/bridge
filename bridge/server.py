"""Main entrypoint for the application."""

import datetime
import os
import random
import string

from azure.storage.blob import BlobClient
from flask import Flask, jsonify, render_template, request, session
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

from bridge import settings
from bridge.azure_sso import AzureSSO

application = Flask(__name__)
application.config.from_object(settings)
Session(application)
sso = AzureSSO(application)
application.jinja_env.globals["now"] = datetime.datetime.utcnow
application.wsgi_app = ProxyFix(application.wsgi_app, x_proto=1, x_host=1)


@application.route("/", methods=["GET", "POST"])
@sso.login_required()
def index() -> None:
    """Index page for the application."""
    ctx = {
        "user": session["user"],
    }
    return render_template("index.html", **ctx)


@application.route("/api/v1/upload", methods=["POST"])
@sso.login_required(api=True)
def upload_file() -> None:
    """Upload a file to Azure Blob Storage."""
    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return jsonify({"error": "missing uploaded file called 'file'"}), 400

    filename = uploaded_file.filename.strip()

    if not filename:
        return jsonify({"error": "Uploaded file missing filename"}), 400

    bits = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
    filename_part, filename_ext = os.path.splitext(uploaded_file.filename)
    filename_part = filename_part.strip()
    blob_name = f"{filename_part}-{bits}{filename_ext}"
    blob = BlobClient.from_connection_string(
        conn_str=settings.CONNECTION_STRING, container_name="bridge", blob_name=blob_name
    )
    blob.upload_blob(uploaded_file.stream)
    return jsonify({"url": blob.url}), 200


@application.route("/livez", methods=["GET"])
def livez() -> int:
    """Health check for the application."""
    return "", 200


@application.route("/readyz", methods=["GET"])
def readyz() -> int:
    """Readiness check for the application."""
    return "", 200


if __name__ == "__main__":
    application.run(port=8000, debug=False)
