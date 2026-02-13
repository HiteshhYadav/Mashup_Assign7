import os
import base64
from flask import Flask, render_template, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)

app = Flask(__name__)


def send_email(to_email):
    zip_file = "mashup.zip"

    # check file exists
    if not os.path.exists(zip_file):
        return False

    # email message
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject="Your Mashup File",
        html_content="Your mashup file is attached."
    )

    # attach zip
    with open(zip_file, "rb") as f:
        data = f.read()

    encoded_file = base64.b64encode(data).decode()

    attachment = Attachment(
        FileContent(encoded_file),
        FileName("mashup.zip"),
        FileType("application/zip"),
        Disposition("attachment")
    )

    message.attachment = attachment

    # send email
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
        return True
    except:
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        email = request.form["email"]

        sent = send_email(email)

        if sent:
            return render_template(
                "success.html",
                message="Mashup sent successfully to your email."
            )
        else:
            return render_template(
                "success.html",
                message="Could not send email right now. Please try again later."
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
