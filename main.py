from flask import Flask, request
from flask import render_template
from resources.resources import Search
from models.package import Pack
from models.tablecreator import TableCreator, TableAds
from flask_restful import Api
# from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
api.add_resource(Search, "/<string:search_items>")
AD_COUNTER = 1
USER_SEARCH = ""

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def home():
    global AD_COUNTER
    global USER_SEARCH
    if request.method == 'GET':
        return render_template("index.html", hide="hidden", placeholder="Unesite pojam...")
    elif request.method == 'POST':
        USER_SEARCH = str(request.form['searchInput'])
        start_storring = Pack(USER_SEARCH).store_ads()
        if start_storring:
            comparator = True
            while comparator:
                ad = TableCreator(name=USER_SEARCH).get_first_item(id=AD_COUNTER)
                if ad:
                    print(ad)
                    oglas = ad[0]
                    return render_template("index.html", ad_name=oglas[1], price=oglas[2], ad_name_href=oglas[5], expires=oglas[4], picture=oglas[3], placeholder=USER_SEARCH)
                AD_COUNTER += 1
        return render_template("index.html", hide="hidden", placeholder="Nema oglasa koji trazite, probajte ponovo...")

@app.route("/store" , methods=['POST'])
def store():
    return render_template("index.html", ad_name="Save")

@app.route("/next" , methods=['POST'])
def next():
    global AD_COUNTER
    global USER_SEARCH
    TableCreator(USER_SEARCH).return_item(AD_COUNTER)
    AD_COUNTER += 1
    return render_template("index.html", ad_name="Pass")


if __name__ == '__main__':
    from db import db
    app.run(port=9090 , debug=True)