from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

from datetime import timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# initialize the API
app = Flask(__name__)
api = Api(app)

# Mood endpoint
class Mood(Resource):
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(258))

    current_streak = db.Column(db.Integer, default=0)
    highest_streak = db.Column(db.Integer, default=0)

    def password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash
    
    def check_password(self, password):
        return check_password_hash(password(self, password), password)

    def get(self):
        data = pd.read_csv('mood.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()  
        
        parser.add_argument('userID', required=True)
        parser.add_argument('Password', required=True) 
        parser.add_argument('name', required=True)
        parser.add_argument('Mood Rating', required=True)
        parser.add_argument('Date', required=True)
        
        args = parser.parse_args()

        data = pd.read_csv('mood.csv')

        streak = 0
        same_entries = data.pivot_table(columns=['userID'], aggfunc='size')

        if same_entries['userID'] == self.username:
            if same_entries['size'] == 0:
                pass
            else:
                change = timedelta(data['Date'])
                streak+=change

        if args['Date'] in list(data['Date']):
            return {
                'message': f"Mood already entered for {args['Date']}"
            }
        else:
            new_data = pd.DataFrame({
                'userID': [args['userID']],
                'Password': [args['Password']],
                'name': [args['name']],
                'Mood Rating': [[]],
                'Data': [args['Date']]
            })
           
            data = data.append(new_data, ignore_index=True)
            data.to_csv('mood.csv', index=False)  
            return {'data': data.to_dict()}, 200

    
api.add_resource(Mood, '/mood')

if __name__ == '__main__':
    app.run()