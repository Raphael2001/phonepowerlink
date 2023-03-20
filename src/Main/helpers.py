from flask_restful import Resource, Api, reqparse, abort
from src.Constas import POWER_LINK_URL
from src.TimeModule.Time import *
import requests
import json
from src.MailsModule.ErrorMail import create_error_mail


def get_task_date(date, added_days, added_hours):
    date = date + timedelta(days=added_days, hours=added_hours)
    if added_hours == 0:
        date = datetime(day=date.day, month=date.month, year=date.year, hour=9, minute=0)
    return date.isoformat()


def get_next_time_for_task():
    now = get_current_time()
    today = now.date()
    day = find_day(today)
    if day == "Friday":
        return get_task_date(now, 2, 0)

    elif day == "Thursday":
        if 17 > now.hour >= 9:
            return get_task_date(now, 0, 1)
        elif 9 > now.hour:
            return get_task_date(now, 0, 0)
        else:
            return get_task_date(now, 3, 0)

    elif day == "Sunday" or day == "Monday" or day == "Tuesday" or day == "Wednesday":
        if 17 > now.hour >= 9:
            return get_task_date(now, 0, 1)
        elif 9 > now.hour:
            return get_task_date(now, 0, 0)
        else:
            return get_task_date(now, 1, 0)
    elif day == "Saturday":
        return get_task_date(now, 1, 0)



class BaseApi(Resource):
    def __init__(self):
        self.uid = None

    def create_headers(self):
        return {"Content-type": "application/json",
                "tokenid": self.uid}


class PowerLinkApi:

    def __init__(self, headers):
        self.headers = headers
        self.phone_number = ""

    def get_client_to_create(self):
        return {
            "accountname": "לקוח חדש " + str(self.phone_number),
            "telephone1": self.phone_number,
        }

    def create_client_with_phone_number(self, phone_number):
        url = POWER_LINK_URL + "record/account"
        self.phone_number = phone_number
        client_to_create = self.get_client_to_create()

        response = requests.post(url, data=json.dumps(client_to_create), headers=self.headers)
        try:
            return json.loads(response.content)
        except Exception as e:
            create_error_mail(response.content)

    def update_phone_record_with_client(self, object_id, account_id):
        url = POWER_LINK_URL + f"record/calllog/{object_id}"
        data = {
            "accountid": account_id
        }
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        return json.loads(response.content)

    def create_task(self,account_id, name):
        url = POWER_LINK_URL + "record/Task"
        data = {
            "objecttypecode": "1",
            "objectid": account_id,
            "subject": "שיחה לא נענתה מ" + name,
            "scheduledend": get_next_time_for_task(),
            "objecttitle": name
        }
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        return json.loads(response.content)

    def get_client_name(self,account_id):
        url = POWER_LINK_URL + f"record/account/{account_id}"
        response = requests.get(url, headers=self.headers)
        return json.loads(response.content)["data"]["Record"]["accountname"]
