'''
TODO : make expire useful
'''

from flask import Flask, request, g, session
from flask import render_template, redirect, url_for
from resources.api_ads import ads_routes
from models.settup_filter_page import First_run, Jeson_results
from models.tablecreator import TableAds
from models.users_services import Users
from db import db, engine

app = Flask(__name__)
app.secret_key = "nestoskrivenos"
app.register_blueprint(ads_routes)
ads_header = ("Slika","Ime", "Cena", "Istice", "Link")

@app.before_request
def create_tables():
    g.user = None
    db.metadata.create_all(engine)
    if 'user_id' in session:
        g.user = session['user_id']

    if 'user_search' in session:
        g.search = session['user_search']

    if 'ad_id' in session:
        g.ad_id = session['ad_id']

    if 'username' in session:
        g.username = session['username']

@app.route('/', methods=['GET','POST'])
def home():
    return render_template("start.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", login_title="Wrong username or password")
    return render_template("login.html", login_title="Login")

@app.route('/logins', methods=['POST', 'GET'])
def logins():
    condition = Users(username=request.form['username'], password=request.form['password']).login()
    if condition:
        session['username'] = request.form['username']
        session['user_id'] = condition
        return redirect(url_for('search_ad'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template("start.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html", signup_title="Username already exists!")
    return render_template("signup.html", signup_title="sign Up")


@app.route('/signups', methods=['POST'])
def signups():
    condition = Users(username=request.form['username'], password=request.form['password']).signup()
    if condition:
        session['username'] = request.form['username']
        session['user_id'] = condition
        return redirect(url_for('search_ad'))
    return redirect(url_for('signup'))

@app.route('/search_ad', methods=['GET','POST'])
def search_ad():
    if request.method == 'GET':
        if g.user:
            return render_template("index.html", hide="hidden", placeholder="Unesite pojam...", username=g.username)
        return render_template("start.html")
    elif request.method == 'POST':
        session['user_search'] = request.form['searchInput'].lower()
        start = First_run(session['user_search'], g.user)
        if start.valid_search():
            ad = TableAds().first_add_that_should_be_seen(start.search, g.user)
            if ad:
                session['ad_id'] = ad.id
                return render_template("index.html", ad_name=ad.name, price=ad.price, ad_name_href=ad.link, expires=ad.expire,
                               picture=ad.picture, placeholder=start.search, username=g.username)
            return render_template("index.html", hide="hidden", placeholder="Pregledani su svi oglasi")
        return render_template("index.html", hide="hidden", placeholder="Nema oglasa")

@app.route("/store" , methods=['POST'])
def store():
    TableAds().update_ad_save_remove(id=g.ad_id, store=2)
    ad = TableAds().first_add_that_should_be_seen(g.search, g.user)
    if ad:
        session['ad_id'] = ad.id
        return render_template("index.html", ad_name=ad.name, price=ad.price, ad_name_href=ad.link, expires=ad.expire,
                           picture=ad.picture, placeholder=g.search, username=g.username)
    return render_template("index.html", hide="hidden", placeholder="Pregledani su svi oglasi")

@app.route("/dont_store" , methods=['GET','POST'])
def dont_store():
    TableAds().update_ad_save_remove(id=g.ad_id, store=0)
    ad = TableAds().first_add_that_should_be_seen(g.search, g.user)
    if ad:
        session['ad_id'] = ad.id
        return render_template("index.html", ad_name=ad.name, price=ad.price, ad_name_href=ad.link, expires=ad.expire,
                           picture=ad.picture, placeholder=g.search, username=g.username)
    return render_template("index.html", hide="hidden", placeholder="Pregledani su svi oglasi")

@app.route("/saved", methods=["GET","POST"])
def saved():
    if not g.user:
        return render_template("start.html")

    if request.method == 'GET':
        search = TableAds().all_search_values(user_id=g.user)
        if search:
            return render_template("saved_unsaved.html", hide="hidden", searches=search, dropdown="Izaberite pretragu", username=g.username)
        return render_template("saved_unsaved.html", hide="hidden", searches=search, dropdown="Jos nista niste pretrazivali", username=g.username)

    if request.method == 'POST':
        search = TableAds().all_search_values(user_id=g.user)
        ad_id, _ = request.form.to_dict().popitem()
        print(session['search'])
        if not ad_id == 'picked':
            TableAds().update_ad_save_remove(ad_id, 0)
        else:
            # session['search'] = _
            g.search = _
            session['search'] = _
        print(session['search'])
        print(g.search)
    saved_ads = TableAds().return_saved_passed(g.search, g.user, 2)
    ads = Jeson_results().pack_json(saved_ads)
    return render_template("saved_unsaved.html", headers=ads_header, ads=ads, searches=search, dropdown=g.search,remove_store="Obrisi", username=g.username)

@app.route("/passed", methods=["GET","POST"])
def passed():
    if not g.user:
        return render_template("start.html")

    if request.method == 'POST':
        ad_id, _ = request.form.to_dict().popitem()
        TableAds().update_ad_save_remove(ad_id, 2)
    saved_ads = TableAds().return_saved_passed(g.search, g.user, 0)
    ads = Jeson_results().pack_json(saved_ads)
    return render_template("saved_unsaved.html", headers=ads_header, ads=ads, remove_store="Sacuvaj", username=g.username)

if __name__ == '__main__':
    app.run(debug=True)