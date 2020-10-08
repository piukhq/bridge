import os
import string
import random
import datetime
from io import BytesIO
from flask_session import Session
from azure.storage.blob import BlobClient
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, session, request

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
def index():
    ctx = {
        "user": session["user"],
    }
    if request.method == "GET":
        return render_template("index.html", **ctx)
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            bits = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
            split = os.path.splitext(uploaded_file.filename)
            blob_name = f"{split[0]}-{bits}{split[1]}"
            blob = BlobClient.from_connection_string(
                conn_str=settings.CONNECTION_STRING, container_name="bridge", blob_name=blob_name
            )
            buffer = BytesIO()
            uploaded_file.save(buffer)
            buffer.seek(0)
            blob.upload_blob(buffer)
        return render_template("upload.html", blob_name=blob.url, **ctx)


# @application.route("/statics")
# def statics():
