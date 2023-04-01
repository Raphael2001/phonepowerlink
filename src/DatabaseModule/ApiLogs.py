import time
from src.DatabaseModule.DataBase import apilogs_ref
from src.MailsModule.ErrorMail import create_error_mail


def add_api_log(url=None, method_name="", status_code=None, body=None, response=None, headers=None, key=None):
    data = {"last_updated": int(time.time()), "method_name": method_name,
            "key": key}
    if url:
        data["url"] = url
    if body:
        data["payload"] = body
    if status_code:
        data["status_code"] = status_code
    if response:
        data["response"] = response
    if headers:
        data["headers"] = headers

    if status_code >=400:
        msg = f"There is a error in {method_name} see the logs for more info"
        create_error_mail(msg)
    apilogs_ref.insert_one(data)
