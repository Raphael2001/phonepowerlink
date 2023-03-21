from flask_restful import reqparse, Resource

from src.Main.helpers import  PowerLinkApi


class Client(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('phonenumber', required=True, location='json', help="phonenumber is missing")
        parser.add_argument('phoneobjectid', required=True, location='json', help="phoneobjectid is missing")
        parser.add_argument('tokenid', required=True, location='json', help="tokenid is missing")

        args = parser.parse_args()
        phone_number = args["phonenumber"]
        phone_object_id = args["phoneobjectid"]
        uid = args["tokenid"]
        power_link = PowerLinkApi(uid)
        response = power_link.create_client_with_phone_number(phone_number)
        account_id = response["data"]["Record"]["accountid"]
        power_link.update_phone_record_with_client(phone_object_id, account_id)
        return {
            'statuscode': 200,
            'body': account_id,
            'message': "",
        }
