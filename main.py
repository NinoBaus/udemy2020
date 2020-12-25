from flask import Flask, request, jsonify, g, session
from flask import render_template, redirect, url_for
from resources.api_ads import ads_routes
from models.settup_filter_page import First_run, Jeson_results
from models.tablecreator import TableAds
from models.users_services import Users
from db import db, engine

app = Flask(__name__)
app.secret_key = "nestoskrivenos"
app.register_blueprint(ads_routes)

@app.before_request
def create_tables():
    g.user = None
    db.metadata.create_all(engine)
    if 'user_id' in session:
        g.user = session['user_id']

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
    session.pop('user_id', None)
    condition = Users(username=request.form['username'], password=request.form['password']).login()
    if condition:
        session['user_id'] = condition
        return redirect(url_for('search_ad'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html", signup_title="Username already exists!")
    return render_template("signup.html", signup_title="sign Up")


@app.route('/signups', methods=['POST'])
def signups():
    session.pop('user_id', None)
    condition = Users(username=request.form['username'], password=request.form['password']).signup()
    if condition:
        session['user_id'] = condition
        return redirect(url_for('search_ad'))
    return redirect(url_for('signup'))

@app.route('/search_ad', methods=['GET','POST'])
def search_ad():
    #user_id is global before I create user_id available once logged in
    global ads
    global prepare
    if request.method == 'GET':
        return render_template("index.html", hide="hidden", placeholder="Unesite pojam...")
    elif request.method == 'POST':
        user_search = str(request.form['searchInput'])
        prepare = First_run(search=user_search, user_id=g.user)
        if prepare.valid_search():
            try:
                ads = prepare.iterate_ads()
                ad = next(ads)
                return render_template("index.html", ad_name=ad[0], price=ad[1], ad_name_href=ad[2], expires=ad[3], picture=ad[4], placeholder=ad[5])
            except StopIteration:
                # import ipdb;                ipdb.set_trace()
                try:
                    ads = prepare.iterate_ads()
                    new_batch = next(ads)
                    return render_template("index.html", ad_name=new_batch[0], price=new_batch[1],
                                           ad_name_href=new_batch[2],
                                           expires=new_batch[3],
                                           picture=new_batch[4], placeholder=new_batch[5])
                except StopIteration:
                    return "Nema vise oglasa"
            except Exception as e:
                return str(e)
        return render_template("index.html", hide="hidden", placeholder="Nema oglasa koji trazite, probajte ponovo...")

@app.route("/store" , methods=['POST'])
def store():
    global ads
    try:
        TableAds().update_ad_save_remove(id=prepare.current_id, store=2)
        ad = next(ads)
        return render_template("index.html", ad_name=ad[0], price=ad[1], ad_name_href=ad[2], expires=ad[3],
                               picture=ad[4], placeholder=ad[5])
    except StopIteration:
        # import ipdb;        ipdb.set_trace()
        try:
            ads = prepare.iterate_ads()
            new_batch = next(ads)
            return render_template("index.html", ad_name=new_batch[0], price=new_batch[1], ad_name_href=new_batch[2],
                                   expires=new_batch[3],
                                   picture=new_batch[4], placeholder=new_batch[5])
        except StopIteration:
            return "Nema vise oglasa"
    except Exception as e:
        print(e)
        return str(e)

@app.route("/dont_store" , methods=['POST'])
def dont_store():
    global ads
    try:
        TableAds().update_ad_save_remove(id=prepare.current_id, store=0)
        ad = next(ads)
        return render_template("index.html", ad_name=ad[0], price=ad[1], ad_name_href=ad[2], expires=ad[3],
                               picture=ad[4], placeholder=ad[5])
    except StopIteration:
        # import ipdb;        ipdb.set_trace()
        try:
            ads = prepare.iterate_ads()
            new_batch = next(ads)
            return render_template("index.html", ad_name=new_batch[0], price=new_batch[1], ad_name_href=new_batch[2], expires=new_batch[3],
                               picture=new_batch[4], placeholder=new_batch[5])
        except StopIteration:
            return "Nema vise oglasa"
    except Exception as e:
        print(e)
        return str(e)

@app.route("/saved", methods=["GET","POST"])
def saved():
    saved_ads = TableAds().return_saved_passed(prepare.search, g.user, 2)
    ads = Jeson_results().pack_json(saved_ads)
    return jsonify({"oglasi": ads})

@app.route("/passed", methods=["GET","POST"])
def passed():
    saved_ads = TableAds().return_saved_passed(prepare.search, g.user, 0)
    ads = Jeson_results().pack_json(saved_ads)
    return jsonify({"oglasi": ads})


if __name__ == '__main__':
    app.run(port=9090, debug=True)