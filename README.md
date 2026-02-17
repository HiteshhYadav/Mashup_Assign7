# Mashup Generator

A small Flask web app that finds audio from YouTube, trims and concatenates clips into a single mashup, zips it, and emails the zip to the provided address.

- Built with: Flask, yt-dlp, pydub, Flask-Mail
- Entry point: `app.py`
- Uses system `ffmpeg` (required by pydub / yt-dlp postprocessing)

---

## Features
- Search YouTube for a given singer/artist and download multiple audio tracks.
- Trim each track to a fixed duration and concatenate them into one mashup.
- Package the mashup into a zip archive and email it as an attachment.
- Simple web form UI (templates/index.html) to submit requests.

---

## Repository structure
- app.py — main Flask application
- requirements.txt — Python dependencies
- Procfile — for deploying with Gunicorn (Heroku compatible)
- templates/index.html — web UI for submitting mashup requests
- templates/success.html — result / message page
- .python-version — suggested Python runtime

---

## Prerequisites

1. Python 3.8+ (use your preferred virtual environment)
2. System-level ffmpeg (required by pydub and yt-dlp postprocessing)

Install ffmpeg:
- macOS (Homebrew): brew install ffmpeg
- Debian/Ubuntu: sudo apt update && sudo apt install -y ffmpeg
- Windows: download from https://ffmpeg.org/download.html and add to PATH

---

## Installation (local development)

1. Clone the repo and change into it:
   git clone https://github.com/HiteshhYadav/Mashup_Assign7.git
   cd Mashup_Assign7

2. Create a virtual environment and activate it:
   python -m venv venv
   # macOS / Linux
   source venv/bin/activate
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

3. Install Python dependencies:
   pip install -r requirements.txt

4. Set SMTP environment variables required by Flask-Mail:
   - MAIL_USERNAME — your SMTP username (email)
   - MAIL_PASSWORD — your SMTP password or app password

   Example (macOS / Linux):
   export MAIL_USERNAME="your-email@example.com"
   export MAIL_PASSWORD="your-smtp-or-app-password"

   Example (Windows PowerShell):
   $env:MAIL_USERNAME="your-email@example.com"
   $env:MAIL_PASSWORD="your-smtp-or-app-password"

Important notes about Gmail:
- If using Gmail, you will likely need to enable an App Password (if you have 2FA enabled) or configure your account appropriately for SMTP access. Do not store credentials in source control.

---

## Running the app

Development (single-process):
python app.py

This starts a development server on http://0.0.0.0:5000

Production with Gunicorn (Procfile provided):
gunicorn app:app

If you use the included Procfile, platform hosts like Heroku will use:
web: gunicorn app:app

---

## How to use the web UI

<img src="assets/interface.png" width="500">

Open https://mashup-assign7.onrender.com/ in your browser and fill the form:

- Singer Name — free text query used to search YouTube
- Number of Videos — integer (must be greater than 10). The app enforces: `num_videos > 10`.
- Duration in Seconds — integer duration of each clip (must be greater than 20). The app enforces: `duration > 20`.
- Email Address — where the resulting mashup zip will be sent.

Behavior:
- The app searches YouTube for the singer, downloads audio for the top N video URLs (using yt-dlp), trims each track to the given duration (in seconds), concatenates them, produces `mashup.mp3`, zips it to `mashup.zip`, sends the zip by email, then cleans up temporary files.

Response messages appear on the success page:
- Validation errors (e.g., number of videos must be > 10)
- Success message when email sent
- Generic error when mashup generation fails


## Success - Mail sent
<img src="assets/mail.png" width="500">
---

## Deployment (Heroku / similar)

1. Ensure Git repo is created and pushed to your hosting platform.
2. The `Procfile` contains:
   web: gunicorn app:app
3. Set environment variables on the platform for `MAIL_USERNAME` and `MAIL_PASSWORD`.
4. Make sure the host provides or you install system `ffmpeg`. On Heroku you can add a buildpack for ffmpeg (see Heroku buildpack community docs).

---

## Troubleshooting & common issues

- ffmpeg not found / pydub errors:
  - Ensure ffmpeg is installed and available in PATH. pydub will fail to read or export audio without ffmpeg.

- "No audio downloaded":
  - The app uses yt-dlp search results. If no valid entries are found, the app raises "No audio downloaded". Try different search terms or increase the search scope.

- yt-dlp download errors:
  - yt-dlp may fail on certain videos due to region or DRM. The app ignores errors for individual downloads and continues.

- SMTP authentication errors:
  - Verify MAIL_USERNAME and MAIL_PASSWORD values and check provider requirements (app password, two-factor authentication, allowed access).
  - If using Gmail, prefer creating an App Password when 2FA is enabled.

- Large jobs / long runtime:
  - Downloading and processing multiple tracks can take time and memory. For many videos or long durations, consider queuing jobs or running in a worker process and returning a job status.

---

## Limitations & Legal / Ethical notice

- This project downloads audio from YouTube programmatically. Ensure you comply with YouTube's Terms of Service and any applicable copyright laws. This code is provided for educational purposes.
- The app does not implement rate-limiting, authentication, or abuse protections. Do not deploy to public internet without adding security, quotas, and abuse controls.

---

## Extending the project (ideas)
- Add job queueing (RQ, Celery) for longer tasks and progress reporting.
- Add authentication and per-user quotas.
- Provide a direct download link instead of emailing the result.
- Allow different transition effects (crossfade) between clips using pydub.

---
