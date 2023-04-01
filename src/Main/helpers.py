from flask_restful import abort
from src.Constas import POWER_LINK_URL
from src.TimeModule.Time import *
import requests
import json
from src.DatabaseModule.ApiLogs import *


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


class OutSideApi:
    def __init__(self, key):
        self.key = key
        self.headers = {}
        self.url = ""
        self.payload = None
        self.method_name = ""

    def post(self):
        response = requests.post(self.url, data=json.dumps(self.payload), headers=self.headers)
        is_success, data = self.handle_response(response)
        return data if is_success else is_success

    def put(self):
        response = requests.put(self.url, data=json.dumps(self.payload), headers=self.headers)
        is_success, data = self.handle_response(response)
        return data if is_success else is_success
    
    def get(self):
        self.payload = None
        response = requests.get(self.url, headers=self.headers)
        is_success, data = self.handle_response(response)
        return data if is_success else is_success

    def handle_response(self, response):
        is_success = True
        if 200 <= response.status_code < 400:
            json_response = json.loads(response.content)
            response_data = json_response

        else:
            response_data = response.content.decode("utf-8")
            is_success = False

        add_api_log(self.url, self.method_name, response.status_code, self.payload, response_data, self.headers,
                    self.key)

        return is_success, response_data


class PowerLinkApi(OutSideApi):

    def __init__(self, uid, call_log_id):

        super().__init__(call_log_id)
        self.phone_number = ""
        self.uid = uid
        self.headers = self.create_headers()

    def create_headers(self):
        return {"Content-type": "application/json",
                "tokenid": self.uid}

    def get_client_to_create(self):
        return {
            "accountname": "לקוח חדש " + str(self.phone_number),
            "telephone1": self.phone_number,
        }

    def create_client_with_phone_number(self, phone_number):
        self.url = POWER_LINK_URL + "record/account"
        self.phone_number = phone_number
        self.payload = self.get_client_to_create()
        self.method_name = "PowerLink - create client"
        return self.post()
     

    def update_phone_record_with_client(self, account_id):
        self.url = POWER_LINK_URL + f"record/calllog/{self.key}"
        self.payload = {
            "accountid": account_id
        }
        self.method_name = "PowerLink - update phone log"
        return self.put()


    def create_task(self, account_id, name):
        self.url = POWER_LINK_URL + "record/Task"
        self.payload = {
            "objecttypecode": "1",
            "objectid": account_id,
            "subject": "שיחה לא נענתה מ" + name,
            "scheduledend": get_next_time_for_task(),
            "objecttitle": name
        }
        self.method_name = "PowerLink - create task"
        return self.post()

    def get_client(self, account_id):
        self.url = POWER_LINK_URL + f"record/account/{account_id}"
        self.method_name = "PowerLink - get client"
        return self.get()


    def get_client_name(self, account_id):
        data = self.get_client(account_id)
        if data:
            return data["data"]["Record"]["accountname"]
        else:
            return data


def abort_api(status_code, message, body=None):
    abort(status_code, status="ERROR", body=body, message=message)


def get_problem_with_api_response():
    return {
        'statuscode': 200,
        'body': {},
        'message': "problem with the request",
    }
