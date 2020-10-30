from app import app
from db import db

db.init_app(app)

#flask decorator for the database
@app.before_first_request
def create_tables():
    db.create_all() #before the first request it will create the db
