import os
import uuid
from datetime import datetime, timezone

import boto3
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

load_dotenv(override=True)

BUCKET = os.environ.get("BUCKET_NAME")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE_NAME")
REGION = os.environ.get("AWS_REGION", "eu-north-1")

session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION,
)

s3 = session.client("s3")
table = session.resource("dynamodb").Table(DYNAMODB_TABLE)

app = Flask(__name__)


@app.route("/")
def index():
    uploads = table.scan().get("Items", [])
    uploads.sort(key=lambda x: x["uploaded_at"], reverse=True)
    return render_template("index.html", uploads=uploads)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and file.filename:
        key = f"{uuid.uuid4()}_{file.filename}"
        s3.upload_fileobj(file, BUCKET, key)
        table.put_item(
            Item={
                "id": key,
                "filename": file.filename,
                "uploaded_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
