import os
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type; utf-8'
app.config['Access-Control-Allow-Origin'] = '*'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

