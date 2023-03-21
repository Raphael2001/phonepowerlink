from src.Main.helpers import  PowerLinkApi
from flask_restful import reqparse, Resource

class Task(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('tokenid', required=True, location='json', help="tokenid is missing")
        parser.add_argument('accountid', required=True, location='json', help="accountid is missing")
        parser.add_argument('name', required=True, location='json', help="name is missing")
        args = parser.parse_args()

        account_id = args["accountid"]
        uid = args["tokenid"]
        name = args["name"]
        PowerLinkApi(uid).create_task(account_id, name)
        return {
            'statuscode': 200,
            'body': account_id,
            'message': "",
        }

