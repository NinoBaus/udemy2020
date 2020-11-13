from flask import Flask, request
from flask import render_template, redirect, url_for
from resources.resources import Search
from models.package import Pack
from models.tablecreator import TableCreator, TableAds
from models.users_services import Users
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
api.add_resource(Search, "/<string:search_items>")
AD_COUNTER = 1
USER_SEARCH = ""
USER_ID = 0

@app.before_request
def create_tables():
    db.metadata.create_all(engine)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template("start.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", login_title="Wrong username or passward")
    return render_template("login.html", login_title="Login")

@app.route('/logins', methods=['POST', 'GET'])
def logins():
    condition = Users(username=request.form['username'], password=request.form['password']).login()
    # print(condition)
    if condition:
        return redirect(url_for('search_ad'))
    return redirect(url_for('login'))

@app.route('/singup', methods=['GET','POST'])
def singup():
    if request.method == 'GET':
        return render_template("singup.html", singup_title="Username already exists!")
    return render_template("singup.html", singup_title="Sing Up")


@app.route('/singups', methods=['POST'])
def singups():
    global USER_ID
    condition = Users(username=request.form['username'], password=request.form['password']).singup()
    if condition:
        USER_ID = condition
        return redirect(url_for('search_ad'))
    return redirect(url_for('singup'))

@app.route('/search_ad', methods=['GET','POST'])
def search_ad():
    global AD_COUNTER
    global USER_SEARCH
    global USER_ID
    if request.method == 'GET':
        return render_template("index.html", hide="hidden", placeholder="Unesite pojam...")
    elif request.method == 'POST':
        USER_SEARCH = str(request.form['searchInput'])
        # print(USER_ID)
        start_storring = Pack(search=USER_SEARCH, user_id=USER_ID).store_ads()
        if start_storring:
            comparator = True
            while comparator:
                ad = TableAds().retrieve_first_item(search=USER_SEARCH,id=AD_COUNTER)
                if ad:
                    return render_template("index.html", ad_name=ad.name, price=ad.price, ad_name_href=ad.link, expires=ad.expire, picture=ad.picture, placeholder=USER_SEARCH)
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
    from db import db, engine
    app.run(port=9090 , debug=True)