from src.Main.helpers import  PowerLinkApi, get_problem_with_api_response
from flask_restful import reqparse, Resource
from src.DatabaseModule.ApiLogs import *


class Phone(Resource):
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
        uid = args["tokenid"]
        name = args["name"]
        add_api_log(method_name="Api - Phone", body=args, key=phone_object_id)

        power_link = PowerLinkApi(uid, phone_object_id)
        if not account_id:
            response = power_link.create_client_with_phone_number(phone_number)
            if not response:
                return get_problem_with_api_response()
            account_id = response["data"]["Record"]["accountid"]
            name = response["data"]["Record"]["accountname"]
            response = power_link.update_phone_record_with_client(account_id)
            if not response:
                return get_problem_with_api_response()
        response = power_link.create_task(account_id, name)
        if not response:
            return get_problem_with_api_response()
        return {
            'statuscode': 200,
            'body': account_id,
            'message': "",
        }
