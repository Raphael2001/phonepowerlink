from requests import get
from MailFunctions import send_message
from src.Constas import ERRORS_RECIPIENTS_MAILS

ip = get('https://api.ipify.org').text


def get_text_n_html(error):
    text = f"sent from my server {ip}"

    html = """
        <html lang="he_IL" dir="rtl">
        <head>
            <style>
                .p {
                    font-size: 18px;
                }
                .span{
                    color:gray;
                    font-size:14px;
                }
            </style>
        </head>

        <body>

                <p>error is  """ + error + """<p>

                <span>sent from my server """ + ip + """ </span>
        </body>

        </html>

        """
    return text, html


def create_error_mail(error):
    text, html = get_text_n_html(error)
    send_message(text, html, ERRORS_RECIPIENTS_MAILS, "Error in Code - Phone PowerLink")
