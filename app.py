def send_email(to_email):
    message = Mail(
        from_email='your_verified_email@gmail.com',
        to_emails=to_email,
        subject='Your Mashup File',
        html_content='Your mashup is attached.'
    )

    with open("mashup.zip", "rb") as f:
        data = f.read()

    import base64
    from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition

    encoded = base64.b64encode(data).decode()

    attachment = Attachment(
        FileContent(encoded),
        FileName('mashup.zip'),
        FileType('application/zip'),
        Disposition('attachment')
    )

    message.attachment = attachment

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)
