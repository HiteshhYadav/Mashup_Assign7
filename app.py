import os
import shutil
import zipfile
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from yt_dlp import YoutubeDL
from pydub import AudioSegment

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

def download_audio(singer, num_videos):
    os.makedirs("downloads", exist_ok=True)

    search_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }

    with YoutubeDL(search_opts) as ydl:
        search = ydl.extract_info(
            f"ytsearch{num_videos * 2}:{singer}",
            download=False
        )

    entries = search.get("entries", [])

    video_urls = []
    for entry in entries:
        if entry and entry.get("_type") == "url" and entry.get("ie_key") == "Youtube":
            video_urls.append(entry["url"])
        if len(video_urls) == num_videos:
            break

    download_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128"
        }]
    }

    with YoutubeDL(download_opts) as ydl:
        for url in video_urls:
            try:
                ydl.download([url])
            except:
                continue


def create_mashup(singer, num_videos, duration):
    os.makedirs("cuts", exist_ok=True)

    download_audio(singer, num_videos)

    for file in os.listdir("downloads"):
        if file.endswith(".mp3"):
            audio_path = os.path.join("downloads", file)
            cut_path = os.path.join("cuts", file)
            audio = AudioSegment.from_mp3(audio_path)
            cut_audio = audio[:duration * 1000]
            cut_audio.export(cut_path, format="mp3")

    final_audio = AudioSegment.empty()

    for file in os.listdir("cuts"):
        if file.endswith(".mp3"):
            audio = AudioSegment.from_mp3(os.path.join("cuts", file))
            final_audio += audio

    output_file = "mashup.mp3"
    final_audio.export(output_file, format="mp3")

    zip_file = "mashup.zip"
    with zipfile.ZipFile(zip_file, "w") as zipf:
        zipf.write(output_file)

    shutil.rmtree("downloads", ignore_errors=True)
    shutil.rmtree("cuts", ignore_errors=True)
    os.remove(output_file)

    return zip_file


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        num_videos = int(request.form["videos"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        if num_videos <= 10:
            return "Number of videos must be greater than 10"

        if duration <= 20:
            return "Duration must be greater than 20 seconds"

        zip_file = create_mashup(singer, num_videos, duration)

        msg = Message(
            subject="Your Mashup File",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        with open(zip_file, "rb") as f:
            msg.attach("mashup.zip", "application/zip", f.read())

        mail.send(msg)

        os.remove(zip_file)

        return render_template("success.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
