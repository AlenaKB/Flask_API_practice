import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
import datetime as dt

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True #flask jwt can raise its own exceptions and messages
app.secret_key = 'cats'
api = Api(app)


jwt = JWTManager(app) #not creating the auth endpoint

@jwt.user_claims_loader
def add_claim(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}
    

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

api.add_resource(UserRegister, '/register')

@app.before_first_request
def create_tables():
    db.create_all()

#db.init_app(app)
if __name__=="__main__":
    db.init_app(app)
    app.run(port = 5000, debug=True)
