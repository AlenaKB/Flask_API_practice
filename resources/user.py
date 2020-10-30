import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required = True,
    help = "This filed cannot be blank")
    parser.add_argument('password',
    type=str,
    required = True,
    help = "This filed cannot be blank")

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"Message": "User already exists"}, 400

        user = UserModel(**data) #because there's the parser username and password are always used
        user.save_to_db()

        return {"message": "User created GREAT SUCCESS"}, 201
