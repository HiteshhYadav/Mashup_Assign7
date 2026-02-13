import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]

        zip_file = "mashup.zip"

        if not os.path.exists(zip_file):
            return "mashup.zip not found"

        msg = Message(
            subject="Your Mashup File",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        with open(zip_file, "rb") as f:
            msg.attach("mashup.zip", "application/zip", f.read())

        mail.send(msg)

        return "Email sent successfully"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
