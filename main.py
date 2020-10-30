from flask import Flask
from flask import request
from flask import render_template
from resources.resources import Search
from flask_restful import Api

from db import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
api.add_resource(Search, "/<string:search_items>")

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'GET':
        return render_template("index.html", hide="hidden")
    else:
        print("Radi")
        return render_template("index.html")



if __name__ == '__main__':
    app.run(port=9090 , debug=True)