from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from db import db
import datetime as dt

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.secret_key = 'cats'
#config JWT to exprire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = dt.timedelta(seconds=1800)


jwt = JWT(app, authenticate, identity_function)

#include user ID in the response body along with an access token
@jwt.auth_response_handler
def custom_response_handler(access_token, identity):
    return jsonify({
                'access_token': access_token.decode('utf-8'),
                'user_id': identity.id
                  })


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

db.init_app(app)
if __name__=="__main__":
    app.run(port = 5000, debug=True)
