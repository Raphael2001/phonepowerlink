import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "bneibrakd@gmail.com"
password = "paqzbfyomiysxgqf"


def create_message(text, html, subject):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


def send_message(text, html, recipients, subject):
    # Create the plain-text and HTML version of your message

    message = create_message(text, html, subject)
    # Create secure connection with server and send email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # pass
        server.login(sender_email, password)
        server.sendmail(
            sender_email, recipients, message.as_string()
        )
