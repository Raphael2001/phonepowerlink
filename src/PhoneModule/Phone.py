from src.Main.helpers import BaseApi, PowerLinkApi
from flask_restful import reqparse

class Phone(BaseApi):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('phonenumber', required=True, location='json', help="phonenumber is missing")
        parser.add_argument('phoneobjectid', required=True, location='json', help="phoneobjectid is missing")
        parser.add_argument('tokenid', required=True, location='json', help="tokenid is missing")
        parser.add_argument('accountid', required=True, location='json', help="accountid is missing")
        parser.add_argument('name', required=True, location='json', help="name is missing")

        args = parser.parse_args()
        account_id = args["accountid"]
        phone_number = args["phonenumber"]
        phone_object_id = args["phoneobjectid"]
        self.uid = args["tokenid"]
        name = args["name"]
        headers = self.create_headers()
        power_link = PowerLinkApi(headers)
        if not account_id:
            response = power_link.create_client_with_phone_number(phone_number)
            account_id = response["data"]["Record"]["accountid"]
            name = response["data"]["Record"]["accountname"]
            power_link.update_phone_record_with_client(phone_object_id, account_id)
        power_link.create_task(account_id, name)
        return {
            'statuscode': 200,
            'body': account_id,
            'message': "",
        }
