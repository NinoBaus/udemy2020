from flask import Flask
from resources.resources import Search
from flask_restful import Api , Resource

from db import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
api.add_resource(Search, "/<string:search_items>")

if __name__ == '__main__':
    app.run(port=9090 , debug=True)