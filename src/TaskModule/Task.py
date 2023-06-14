from src.Main.helpers import PowerLinkApi, get_problem_with_api_response
from flask_restful import reqparse, Resource
from src.DatabaseModule.ApiLogs import *


class Task(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('tokenid', required=True, location='json', help="tokenid is missing")
        parser.add_argument('accountid', required=True, location='json', help="accountid is missing")
        parser.add_argument('name', required=True, location='json', help="name is missing")
        parser.add_argument('phoneobjectid', required=True, location='json', help="phoneobjectid is missing")
        parser.add_argument('tasktype', required=True, location='json', help="tasktype is missing")
        args = parser.parse_args()

        account_id = args["accountid"]
        uid = args["tokenid"]
        name = args["name"]
        call_log_id = args["phoneobjectid"]
        task_type = args["tasktype"]
        add_api_log(method_name="Api - Task", body=args, key=call_log_id)

        response = PowerLinkApi(uid, call_log_id).create_task(account_id, name, task_type)
        if not response:
            return get_problem_with_api_response()
        return {
            'statuscode': 200,
            'body': account_id,
            'message': "",
        }
