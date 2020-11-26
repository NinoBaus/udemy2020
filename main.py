from flask import Flask, request
from flask import render_template, redirect, url_for
from resources.resources import Search
from models.settup_filter_page import First_run
from models.tablecreator import TableAds
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
    global USER_ID
    condition = Users(username=request.form['username'], password=request.form['password']).login()
    if condition:
        USER_ID = condition
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
    #user_id is global before I create user_id available once logged in
    global USER_ID
    global ads
    global prepare
    if request.method == 'GET':
        return render_template("index.html", hide="hidden", placeholder="Unesite pojam...")
    elif request.method == 'POST':
        user_search = str(request.form['searchInput'])
        prepare = First_run(search=user_search, user_id=USER_ID)
        if prepare.valid_search():
            try:
                ads = prepare.iterate_ads()
                ad = next(ads)
                return render_template("index.html", ad_name=ad[0], price=ad[1], ad_name_href=ad[2], expires=ad[3], picture=ad[4], placeholder=ad[5])
            except StopIteration:
                return "Nema vise oglasa \o/"
        return render_template("index.html", hide="hidden", placeholder="Nema oglasa koji trazite, probajte ponovo...")

@app.route("/store" , methods=['POST'])
def store():
    global prepare
    global ads
    try:
        TableAds().update_ad_save_remove(id=prepare.current_id, store=2)
        ad = next(ads)
        return render_template("index.html", ad_name=ad[0], price=ad[1], ad_name_href=ad[2], expires=ad[3],
                               picture=ad[4], placeholder=ad[5])
    except StopIteration:
        return "Nema vise oglasa bro"

@app.route("/dont_store" , methods=['POST'])
def dont_store():
    global prepare
    global ads
    try:
        TableAds().update_ad_save_remove(id=prepare.current_id, store=0)
        ad = next(ads)
        return render_template("index.html", ad_name=ad[0], price=ad[1], ad_name_href=ad[2], expires=ad[3],
                               picture=ad[4], placeholder=ad[5])
    except StopIteration:
        return "Nema vise oglasa bro"


if __name__ == '__main__':
    from db import db, engine
    app.run(port=9090 , debug=True)