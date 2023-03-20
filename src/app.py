import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse, abort
from src.ClientModule.Client import Client
from src.TaskModule.Task import Task
from src.PhoneModule.Phone import Phone


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type; utf-8'
app.config['Access-Control-Allow-Origin'] = '*'

api.add_resource(Phone, '/api/v1/phone')
api.add_resource(Client, '/api/v1/client')
api.add_resource(Task, '/api/v1/task')

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

