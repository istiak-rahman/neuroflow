from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

# initialize the API
app = Flask(__name__)
api = Api(app)

# Mood endpoint
class Mood(Resource):
    def get(self):
        data = pd.read_csv('mood.csv')
        data = data.to_dict()
        return {'data': data}, 200

api.add_resource(Mood, '/mood')

if __name__ == '__main__':
    app.run()